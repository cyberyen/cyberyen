#!/usr/bin/env python3
# Copyright (c) 2019-2020 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Cyberyen aliases -chain=signet to testnet params (CreateChainParams TODO).

Does not implement a real Signet challenge/genesis; only asserts the shipped alias.
"""

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal


# CTestNetParams genesis (chainparams.cpp); signet CreateChainParams returns CTestNetParams.
TESTNET_GENESIS = "fc87d3af1c388f561386e08cfb74819cc04cf33ddb6c39f0bfb685048d3dfb2a"


class SignetBasicTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1
        self.setup_clean_chain = True
        # Datadir / cookie paths use BaseParams DataDir ("signet").
        self.chain = "signet"
        # Regtest deterministic WIFs are invalid under the testnet alias.
        self.extra_args = [["-disablewallet"]]

    def setup_nodes(self):
        self.add_nodes(self.num_nodes, self.extra_args)
        self.start_nodes()

    def run_test(self):
        # Node starts: signet is a recognized -chain value (not "Unknown chain").
        info = self.nodes[0].getblockchaininfo()
        # Consensus params come from the testnet alias.
        assert_equal(info["chain"], "test")
        assert_equal(info["blocks"], 0)
        genesis = self.nodes[0].getblockhash(0)
        assert_equal(genesis, TESTNET_GENESIS)


if __name__ == '__main__':
    SignetBasicTest().main()
