#!/usr/bin/env python3
# Copyright (c) 2014-2020 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test logic for skipping signature validation on old blocks.

Test logic for skipping signature validation on blocks which we've assumed
valid (https://github.com/bitcoin/bitcoin/pull/9484)

We build a chain that includes and invalid signature for one of the
transactions:

    0:        genesis block
    1:        block 1 with coinbase transaction output.
    2-101:    bury that block with 100 blocks so the coinbase transaction
              output can be spent
    102:      a block containing a transaction spending the coinbase
              transaction output. The transaction has an invalid signature.
    103+:     bury the bad block with just over two weeks' work
              (GetBlockProofEquivalentTime vs nPowTargetSpacing=60).

Start three nodes:

    - node0 has no -assumevalid parameter. After headers of the full chain
      are present, connecting block 102 is rejected; the tip stays at 101.
    - node1 has -assumevalid set to the hash of block 102. With the full
      header tree (so pindexBestHeader is two weeks ahead) it accepts the
      whole chain.
    - node2 has -assumevalid set to the hash of block 102 but only sees
      200 headers. Block 102 is still validated and rejected.

Headers and bodies are submitted over RPC. Twenty thousand unsolicited
P2P header messages disconnects; leftover Bitcoin's 2100-header dump does
not recode onto Cyberyen 60s spacing.
"""
from test_framework.blocktools import (
    create_block,
    create_coinbase,
    get_block_subsidy,
    REGTEST_POW_TARGET_SPACING,
)
from test_framework.key import ECKey
from test_framework.messages import (
    CBlockHeader,
    COIN,
    COutPoint,
    CTransaction,
    CTxIn,
    CTxOut,
)
from test_framework.script import (CScript, OP_TRUE)
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal


class AssumeValidTest(BitcoinTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 3
        self.rpc_timeout = 120
        # Python blocks have no HogEx; keep MWEB never-active (existing pattern).
        self.extra_args = [['-vbparams=mweb:-2:0'] for _ in range(3)]

    def setup_network(self):
        self.add_nodes(3, extra_args=self.extra_args)
        # Start node0. We don't start the other nodes yet since
        # we need to pre-mine a block with an invalid transaction
        # signature so we can pass in the block hash as assumevalid.
        self.start_node(0)

    def submit_headers(self, node, blocks):
        for block in blocks:
            node.submitheader(CBlockHeader(block).serialize().hex())

    def submit_blocks_until(self, node, blocks, last_index):
        """submitblock from blocks[0] through last_index inclusive."""
        for block in blocks[:last_index + 1]:
            node.submitblock(block.serialize().hex())

    def run_test(self):
        # Build the blockchain
        self.tip = int(self.nodes[0].getbestblockhash(), 16)
        self.block_time = self.nodes[0].getblock(self.nodes[0].getbestblockhash())['time'] + 1

        self.blocks = []

        # Get a pubkey for the coinbase TXO
        coinbase_key = ECKey()
        coinbase_key.generate()
        coinbase_pubkey = coinbase_key.get_pubkey().get_bytes()

        # Create the first block with a coinbase output to our key
        height = 1
        block = create_block(self.tip, create_coinbase(height, coinbase_pubkey), self.block_time, version=0x20000000)
        self.blocks.append(block)
        self.block_time += 1
        block.solve()
        # Save the coinbase for later
        self.block1 = block
        self.tip = block.sha256
        height += 1

        # Bury the block 100 deep so the coinbase output is spendable
        for _ in range(100):
            block = create_block(self.tip, create_coinbase(height), self.block_time, version=0x20000000)
            block.solve()
            self.blocks.append(block)
            self.tip = block.sha256
            self.block_time += 1
            height += 1

        # Create a transaction spending the coinbase output with an invalid (null) signature
        tx = CTransaction()
        tx.vin.append(CTxIn(COutPoint(self.block1.vtx[0].sha256, 0), scriptSig=b""))
        tx.vout.append(CTxOut(get_block_subsidy(1) - COIN, CScript([OP_TRUE])))
        tx.calc_sha256()

        block102 = create_block(self.tip, create_coinbase(height), self.block_time, version=0x20000000)
        self.block_time += 1
        block102.vtx.extend([tx])
        block102.hashMerkleRoot = block102.calc_merkle_root()
        block102.rehash()
        block102.solve()
        self.blocks.append(block102)
        self.tip = block102.sha256
        self.block_time += 1
        height += 1

        # Bury the assumed valid block with just over two weeks of work.
        # GetBlockProofEquivalentTime = height_delta * nPowTargetSpacing (regtest 60s).
        two_weeks = 60 * 60 * 24 * 7 * 2
        bury = two_weeks // REGTEST_POW_TARGET_SPACING + 1
        for _ in range(bury):
            # 0x20000000 is in CPureBlockHeader::IsLegacy; 0x20000002 is not and is high-hash.
            block = create_block(self.tip, create_coinbase(height), self.block_time, version=0x20000000)
            block.solve()
            self.blocks.append(block)
            self.tip = block.sha256
            self.block_time += 1
            height += 1
        tip_height = 101 + 1 + bury  # 100 bury-to-mature + invalid block 102 + two-weeks bury

        # Start node1 and node2 with assumevalid so they accept a block with a bad signature.
        assume = ["-assumevalid=" + hex(block102.sha256)]
        self.start_node(1, extra_args=self.extra_args[1] + assume)
        self.start_node(2, extra_args=self.extra_args[2] + assume)

        # Headers first so pindexBestHeader sits at the two-week tip before bodies connect.
        self.submit_headers(self.nodes[0], self.blocks)
        self.submit_headers(self.nodes[1], self.blocks)
        self.submit_headers(self.nodes[2], self.blocks[:200])
        assert_equal(self.nodes[0].getblockchaininfo()['headers'], tip_height)
        assert_equal(self.nodes[1].getblockchaininfo()['headers'], tip_height)
        assert_equal(self.nodes[2].getblockchaininfo()['headers'], 200)

        # node0: no assumevalid. Block 102 (index 101) is rejected.
        self.submit_blocks_until(self.nodes[0], self.blocks, 101)
        assert_equal(self.nodes[0].getblockcount(), 101)

        # node1: assumevalid + two weeks of headers. All blocks accepted.
        self.submit_blocks_until(self.nodes[1], self.blocks, len(self.blocks) - 1)
        assert_equal(self.nodes[1].getblockcount(), tip_height)

        # node2: assumevalid, but not buried. Block 102 rejected.
        self.submit_blocks_until(self.nodes[2], self.blocks, 199)
        assert_equal(self.nodes[2].getblockcount(), 101)


if __name__ == '__main__':
    AssumeValidTest().main()
