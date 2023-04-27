// Copyright (c) 2014-2019 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <arith_uint256.h>
#include <chainparams.h>
#include <net.h>
#include <signet.h>
#include <validation.h>

#include <test/util/setup_common.h>

#include <boost/test/unit_test.hpp>

BOOST_FIXTURE_TEST_SUITE(validation_tests, TestingSetup)

/**
 * the maximum block reward at a given height for a block without fees
 */
uint64_t expectedMaxSubsidy(int height) {
    if (height < 99000) {
	return 1000000 * COIN;
    } else if (height < 100000) {
	return 500000 * COIN;
    } else if (height < 200000) {
	return 250000 * COIN;
    } else if (height < 300000) {
	return 125000 * COIN;
    } else if (height < 400000) {
	return  62500 * COIN;
    } else if (height < 500000) {
	return  31250 * COIN;
    } else if (height < 600000) {
	return  15625 * COIN;
    } else {
	return  10000 * COIN;
    }
}

/**
 * the minimum possible value for the maximum block reward at a given height
 * for a block without fees
 */
uint64_t expectedMinSubsidy(int height) {
    if (height < 99000) {
	return 0;
    } else if (height < 100000) {
	return 0;
    } else if (height < 200000) {
	return 250000 * COIN;
    } else if (height < 300000) {
	return 125000 * COIN;
    } else if (height < 400000) {
	return  62500 * COIN;
    } else if (height < 500000) {
	return  31250 * COIN;
    } else if (height < 600000) {
	return  15625 * COIN;
    } else {
	return  10000 * COIN;
    }
}

BOOST_AUTO_TEST_CASE(subsidy_limit_test)
{
    int nHeight = 0;
    int nStepSize= 1;
    const auto chainParams = CreateChainParams(*m_node.args, CBaseChainParams::MAIN);
    //const Consensus::Params& params = Params(CBaseChainParams::MAIN).GetConsensus();
    CAmount nSum = 0;

    for (nHeight = 0; nHeight <= 99000; nHeight++) {
      CAmount nSubsidy = GetBlockSubsidy(nHeight, chainParams->GetConsensus());
	BOOST_CHECK(MoneyRange(nSubsidy));
	BOOST_CHECK(nSubsidy <= 1000000 * COIN);
	nSum += nSubsidy * nStepSize;
    }
    for (; nHeight <= 100000; nHeight++) {
      CAmount nSubsidy = GetBlockSubsidy(nHeight, chainParams->GetConsensus());
	BOOST_CHECK(MoneyRange(nSubsidy));
	BOOST_CHECK(nSubsidy <= 500000 * COIN);
	nSum += nSubsidy * nStepSize;
    }
    for (; nHeight < 600000; nHeight++) {
      CAmount nSubsidy = GetBlockSubsidy(nHeight, chainParams->GetConsensus());
	CAmount nExpectedSubsidy = (500000 >> (nHeight / 100000)) * COIN;
	BOOST_CHECK(MoneyRange(nSubsidy));
	BOOST_CHECK(nSubsidy == nExpectedSubsidy);
	nSum += nSubsidy * nStepSize;
    }

    //test sum +- ~10billion
    arith_uint256 upperlimit = arith_uint256("95e14ec776380000"); //108 billion cy
    BOOST_CHECK(nSum <= upperlimit);

    arith_uint256 lowerlimit = arith_uint256("7a1fe16027700000"); //88 billion cy
    BOOST_CHECK(nSum >= lowerlimit);

    // Test reward at 600k+ is constant
    CAmount nConstantSubsidy = GetBlockSubsidy(600000, chainParams->GetConsensus());
    BOOST_CHECK(nConstantSubsidy == 10000 * COIN);

    nConstantSubsidy = GetBlockSubsidy(700000, chainParams->GetConsensus());
    BOOST_CHECK(nConstantSubsidy == 10000 * COIN);
}

BOOST_AUTO_TEST_SUITE_END()
