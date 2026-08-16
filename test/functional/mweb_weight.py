#!/usr/bin/env python3
# Copyright (c) 2021 The Cyberyen Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""MWEB block weight test"""

from decimal import Decimal

from test_framework.cy_util import setup_mweb_chain
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal

class MWEBWeightTest(BitcoinTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = True
        self.rpc_timeout = 120
        self.num_nodes = 3
        self.extra_args = [["-spendzeroconfchange=0"]] * self.num_nodes

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    def run_test(self):
        # Max number of MWEB transactions in a block (20000/39)
        tx_limit = 512

        self.log.info("Activate MWEB")
        setup_mweb_chain(self.nodes[0])
        self.sync_all()

        self.log.info("Create confirmed transparent UTXOs for the spending nodes")
        node1_outs = {self.nodes[1].getnewaddress(): 2 for _ in range(tx_limit)}
        self.nodes[0].sendmany("", node1_outs)
        node2_outs = {self.nodes[2].getnewaddress(): 2 for _ in range(tx_limit + 1)}
        self.nodes[0].sendmany("", node2_outs)
        self.nodes[0].generate(1)
        self.sync_all()

        self.log.info("Create transactions up to the max block weight")
        addr = self.nodes[0].getnewaddress(address_type='mweb')
        for x in range(0, tx_limit):
            self.nodes[1].sendtoaddress(addr, 1)
        assert_equal(len(self.nodes[1].getrawmempool()), tx_limit)

        self.log.info("Create a block")
        self.nodes[1].generate(1)
        self.sync_all()

        self.log.info("Check mempool is empty")
        assert_equal(len(self.nodes[1].getrawmempool()), 0)

        self.log.info("Check UTXOs have matured")
        utxos = self.nodes[0].listunspent(addresses=[addr])
        assert_equal(len(utxos), tx_limit)
        assert all(x['amount'] == 1 and x['spendable'] for x in utxos)

        self.log.info("Create transactions exceeding the max block weight")
        addr = self.nodes[0].getnewaddress(address_type='mweb')
        for x in range(0, tx_limit + 1):
            self.nodes[2].sendtoaddress(addr, 0.01)
        assert_equal(len(self.nodes[2].getrawmempool()), tx_limit + 1)

        self.log.info("Create a block")
        self.nodes[2].generate(1)
        self.sync_all()

        self.log.info("Check mempool is not empty")
        assert_equal(len(self.nodes[2].getrawmempool()), 1)

        self.log.info("Check UTXOs have matured")
        utxos = self.nodes[0].listunspent(addresses=[addr])
        assert_equal(len(utxos), tx_limit)
        assert all(x['amount'] == Decimal('0.01') and x['spendable'] for x in utxos)

if __name__ == '__main__':
    MWEBWeightTest().main()
