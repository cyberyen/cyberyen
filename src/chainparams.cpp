// Copyright (c) 2010 Satoshi Nakamoto
// Copyright (c) 2009-2020 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <chainparams.h>

#include <chainparamsseeds.h>
#include <consensus/merkle.h>
#include <hash.h> // for signet block challenge hash
#include <tinyformat.h>
#include <util/system.h>
#include <util/strencodings.h>
#include <versionbitsinfo.h>

#include <assert.h>

#include <boost/algorithm/string/classification.hpp>
#include <boost/algorithm/string/split.hpp>

static CBlock CreateGenesisBlock(const char* pszTimestamp, const CScript& genesisOutputScript, uint32_t nTime, uint32_t nNonce, uint32_t nBits, int32_t nVersion, const CAmount& genesisReward)
{
    CMutableTransaction txNew;
    txNew.nVersion = 1;
    txNew.vin.resize(1);
    txNew.vout.resize(1);
    txNew.vin[0].scriptSig = CScript() << 486604799 << CScriptNum(4) << std::vector<unsigned char>((const unsigned char*)pszTimestamp, (const unsigned char*)pszTimestamp + strlen(pszTimestamp));
    txNew.vout[0].nValue = genesisReward;
    txNew.vout[0].scriptPubKey = genesisOutputScript;

    CBlock genesis;
    genesis.nTime    = nTime;
    genesis.nBits    = nBits;
    genesis.nNonce   = nNonce;
    genesis.nVersion = nVersion;
    genesis.vtx.push_back(MakeTransactionRef(std::move(txNew)));
    genesis.hashPrevBlock.SetNull();
    genesis.hashMerkleRoot = BlockMerkleRoot(genesis);
    return genesis;
}

/**
 * Build the genesis block. Note that the output of its generation
 * transaction cannot be spent since it did not originally exist in the
 * database.
 *
 * CBlock(hash=000000000019d6, ver=1, hashPrevBlock=00000000000000, hashMerkleRoot=4a5e1e, nTime=1231006505, nBits=1d00ffff, nNonce=2083236893, vtx=1)
 *   CTransaction(hash=4a5e1e, ver=1, vin.size=1, vout.size=1, nLockTime=0)
 *     CTxIn(COutPoint(000000, -1), coinbase 04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73)
 *     CTxOut(nValue=50.00000000, scriptPubKey=0x5F1DF16B2B704C8A578D0B)
 *   vMerkleTree: 4a5e1e
 */
static CBlock CreateGenesisBlock(uint32_t nTime, uint32_t nNonce, uint32_t nBits, int32_t nVersion, const CAmount& genesisReward)
{
    const char* pszTimestamp = "The Dark Side of the Moon 2022";
    const CScript genesisOutputScript = CScript() << ParseHex("040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9") << OP_CHECKSIG;
    return CreateGenesisBlock(pszTimestamp, genesisOutputScript, nTime, nNonce, nBits, nVersion, genesisReward);
}

/**
 * Main network
 */
class CMainParams : public CChainParams {
public:
    CMainParams() {
	strNetworkID = CBaseChainParams::MAIN;
	consensus.signet_blocks = false;
	consensus.signet_challenge.clear();
	consensus.nSubsidyHalvingInterval = 100000;
	consensus.powLimit = uint256S("00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff");
	consensus.nPowTargetTimespan = 4 * 60 * 60;
	consensus.nPowTargetSpacing = 1 * 60;
	consensus.fPowAllowMinDifficultyBlocks = false;
	consensus.fPowNoRetargeting = false;
	consensus.nRuleChangeActivationThreshold = 9576; // 95%
	consensus.nMinerConfirmationWindow = 10080; // nPowTargetTimespan / nPowTargetSpacing * 4

	/**
	 * The message start string is designed to be unlikely to occur in normal data.
	 * The characters are rarely used upper ASCII, not valid as UTF-8, and produce
	 * a large 32-bit integer with any alignment.
	 */
	pchMessageStart[0] = 0xc1;
	pchMessageStart[1] = 0xc1;
	pchMessageStart[2] = 0xc1;
	pchMessageStart[3] = 0xc1;
	nDefaultPort = 58383;
	nPruneAfterHeight = 100000;
	m_assumed_blockchain_size = 40;
	m_assumed_chain_state_size = 2;

	genesis = CreateGenesisBlock(1659708882, 2000096520, 0x1e0ffff0, 1, 1000000 * COIN); // new value
	consensus.hashGenesisBlock = genesis.GetHash();
	assert(consensus.hashGenesisBlock == uint256S("0x34458c96bb547193fa90b2f2599056684b0083d8a2996f2025943eb545031d29"));
	assert(genesis.hashMerkleRoot == uint256S("0x7055a6ae72bdfdaafaac2619d61684e037f477870d70951bd3bf6964d36bc405"));

	// Note that of those which support the service bits prefix, most only support a subset of
	// possible options.
	// This is fine at runtime as we'll fall back to using them as an addrfetch if they don't support the
	// service bits we want, but we should get them updated to support all service bits wanted by any
	// release ASAP to avoid it where possible.
	vSeeds.emplace_back("cyberyen.org");
	vSeeds.emplace_back("dnsseed.cyberyen.work");

	base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,28);
	base58Prefixes[SCRIPT_ADDRESS] = std::vector<unsigned char>(1,77);
	base58Prefixes[SCRIPT_ADDRESS2] = std::vector<unsigned char>(1,22);
	base58Prefixes[SECRET_KEY] =     std::vector<unsigned char>(1,156);
	base58Prefixes[EXT_PUBLIC_KEY] = {0x01, 0x88, 0xB2, 0x1E};
	base58Prefixes[EXT_SECRET_KEY] = {0x01, 0x88, 0xAD, 0xE4};

	bech32_hrp = "cy";
	mweb_hrp = "cymweb";

	vFixedSeeds = std::vector<uint8_t>(std::begin(chainparams_seed_main), std::end(chainparams_seed_main));

	fDefaultConsistencyChecks = false;
	fRequireStandard = true;
	m_is_test_chain = false;
	m_is_mockable_chain = false;

	checkpointData = {
	  {
	    {  0, uint256S("0x34458c96bb547193fa90b2f2599056684b0083d8a2996f2025943eb545031d29")},

	  }
	};


	chainTxData = ChainTxData{
	  // Data from rpc: getchaintxstats 4096 62e2e3d21343a00994d38a63524867507dbeee6850e8fbf02e9c47a3ccf82f24
	  /* nTime    */ 1659708882,
	  /* nTxCount */ 0,
	  /* dTxRate  */ 0.29
	};
    }
};

/**
 * Testnet (v3)
 */
class CTestNetParams : public CChainParams {
public:
    CTestNetParams() {
	strNetworkID = CBaseChainParams::TESTNET;
	consensus.signet_blocks = false;
	consensus.signet_challenge.clear();
	consensus.nSubsidyHalvingInterval = 100000;
	consensus.BIP16Height = 0; // always enforce P2SH BIP16 on testnet
	consensus.powLimit = uint256S("00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff");
	consensus.nPowTargetTimespan = 4 * 60 * 60;
	consensus.nPowTargetSpacing = 1 * 60;
	consensus.fPowAllowMinDifficultyBlocks = true;
	consensus.fPowNoRetargeting = false;
	consensus.nRuleChangeActivationThreshold = 2880; // 2 days (note this is significantly lower than Bitcoin standard)
	consensus.nMinerConfirmationWindow = 10080; // 60 * 24 * 7 = 10,080 blocks, or one week

	pchMessageStart[0] = 0xfc;
	pchMessageStart[1] = 0xc1;
	pchMessageStart[2] = 0xb7;
	pchMessageStart[3] = 0xdc;
	nDefaultPort = 44551;
	nPruneAfterHeight = 1000;
	m_assumed_blockchain_size = 4;
	m_assumed_chain_state_size = 1;

	genesis = CreateGenesisBlock(1659708882, 223176, 0x1e0ffff0, 1, 1000000 * COIN);
	consensus.hashGenesisBlock = genesis.GetHash();
	assert(consensus.hashGenesisBlock == uint256S("0xfc87d3af1c388f561386e08cfb74819cc04cf33ddb6c39f0bfb685048d3dfb2a"));
	assert(genesis.hashMerkleRoot == uint256S("0x7055a6ae72bdfdaafaac2619d61684e037f477870d70951bd3bf6964d36bc405"));

	vFixedSeeds.clear();
	vSeeds.clear();
	// nodes with support for servicebits filtering should be at the top
	vSeeds.emplace_back("dnsseed-test.cyberyen.work");

	base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,112);
	base58Prefixes[SCRIPT_ADDRESS] = std::vector<unsigned char>(1,196);
	base58Prefixes[SCRIPT_ADDRESS2] = std::vector<unsigned char>(1,58);
	base58Prefixes[SECRET_KEY] =     std::vector<unsigned char>(1,240);
	base58Prefixes[EXT_PUBLIC_KEY] = {0x04, 0x35, 0x87, 0xCF};
	base58Prefixes[EXT_SECRET_KEY] = {0x04, 0x35, 0x83, 0x94};

	bech32_hrp = "tcy";
	mweb_hrp = "tmweb";

	vFixedSeeds = std::vector<uint8_t>(std::begin(chainparams_seed_test), std::end(chainparams_seed_test));

	fDefaultConsistencyChecks = false;
	fRequireStandard = false;
	m_is_test_chain = true;
	m_is_mockable_chain = false;

	checkpointData = {
	    {
	      {  0, uint256S("0xfc87d3af1c388f561386e08cfb74819cc04cf33ddb6c39f0bfb685048d3dfb2a")},

	    }
	};

	chainTxData = ChainTxData{
	    // Data from RPC: getchaintxstats 4096 36d8ad003bac090cf7bf4e24fbe1d319554c8933b9314188d6096ac12648764d
	   /* nTime    */ 1659708882,
	   /* nTxCount */ 0,
	   /* dTxRate  */ 0.01,
	};
    }
};

/**
 * Regression test
 */
class CRegTestParams : public CChainParams {
public:
    explicit CRegTestParams(const ArgsManager& args) {
	strNetworkID =  CBaseChainParams::REGTEST;
	consensus.signet_blocks = false;
	consensus.signet_challenge.clear();
	consensus.nSubsidyHalvingInterval = 150;
	consensus.BIP16Height = 0;
	consensus.nPowTargetTimespan = 4 * 60 * 60; // 3.5 days
	consensus.nPowTargetSpacing = 1 * 60;
	consensus.fPowAllowMinDifficultyBlocks = true;
	consensus.fPowNoRetargeting = true;
	consensus.nRuleChangeActivationThreshold = 540; // 75% for testchains
	consensus.nMinerConfirmationWindow = 720;
	consensus.nMinimumChainWork = uint256{};
	consensus.defaultAssumeValid = uint256{};

	pchMessageStart[0] = 0xfa;
	pchMessageStart[1] = 0xbf;
	pchMessageStart[2] = 0xb5;
	pchMessageStart[3] = 0xda;
	nDefaultPort = 18440;
	nPruneAfterHeight = 1000;
	m_assumed_blockchain_size = 0;
	m_assumed_chain_state_size = 0;

	UpdateActivationParametersFromArgs(args);

	genesis = CreateGenesisBlock(1659708882, 4, 0x207fffff, 1, 1000000 * COIN);
	consensus.hashGenesisBlock = genesis.GetHash();
	assert(consensus.hashGenesisBlock == uint256S("0x69d049e08f8eb4e26290d8f4ad379aa237cd3aab158a42e2ee6c615815a17e62"));
	assert(genesis.hashMerkleRoot == uint256S("0x7055a6ae72bdfdaafaac2619d61684e037f477870d70951bd3bf6964d36bc405"));

	vFixedSeeds.clear(); //!< Regtest mode doesn't have any fixed seeds.
	vSeeds.clear();      //!< Regtest mode doesn't have any DNS seeds.

	fDefaultConsistencyChecks = true;
	fRequireStandard = true;
	m_is_test_chain = true;
	m_is_mockable_chain = true;

	checkpointData = {
	    {
	      {  0, uint256S("0x69d049e08f8eb4e26290d8f4ad379aa237cd3aab158a42e2ee6c615815a17e62")},

	    }
	};

	chainTxData = ChainTxData{
	    0,
	    0,
	    0
	};

	base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,111);
	base58Prefixes[SCRIPT_ADDRESS] = std::vector<unsigned char>(1,196);
	base58Prefixes[SCRIPT_ADDRESS2] = std::vector<unsigned char>(1,58);
	base58Prefixes[SECRET_KEY] =     std::vector<unsigned char>(1,239);
	base58Prefixes[EXT_PUBLIC_KEY] = {0x04, 0x35, 0x87, 0xCF};
	base58Prefixes[EXT_SECRET_KEY] = {0x04, 0x35, 0x83, 0x94};

	bech32_hrp = "rcy";
	mweb_hrp = "tmweb";
    }

    /**
     * Allows modifying the Version Bits regtest parameters.
     */
    void UpdateVersionBitsParameters(Consensus::DeploymentPos d, int64_t nStartTime, int64_t nTimeout, int64_t nStartHeight, int64_t nTimeoutHeight)
    {
	consensus.vDeployments[d].nStartTime = nStartTime;
	consensus.vDeployments[d].nTimeout = nTimeout;
	consensus.vDeployments[d].nStartHeight = nStartHeight;
	consensus.vDeployments[d].nTimeoutHeight = nTimeoutHeight;
    }
    void UpdateActivationParametersFromArgs(const ArgsManager& args);
};

void CRegTestParams::UpdateActivationParametersFromArgs(const ArgsManager& args)
{
    if (args.IsArgSet("-segwitheight")) {
	int64_t height = args.GetArg("-segwitheight", consensus.SegwitHeight);
	if (height < -1 || height >= std::numeric_limits<int>::max()) {
	    throw std::runtime_error(strprintf("Activation height %ld for segwit is out of valid range. Use -1 to disable segwit.", height));
	} else if (height == -1) {
	    LogPrintf("Segwit disabled for testing\n");
	    height = std::numeric_limits<int>::max();
	}
	consensus.SegwitHeight = static_cast<int>(height);
    }

    if (!args.IsArgSet("-vbparams")) return;

    for (const std::string& strDeployment : args.GetArgs("-vbparams")) {
	std::vector<std::string> vDeploymentParams;
	boost::split(vDeploymentParams, strDeployment, boost::is_any_of(":"));
	if (vDeploymentParams.size() < 3 || 5 < vDeploymentParams.size()) {
	    throw std::runtime_error("Version bits parameters malformed, expecting deployment:start:end[:heightstart:heightend]");
	}
	int64_t nStartTime, nTimeout, nStartHeight, nTimeoutHeight;
	if (!ParseInt64(vDeploymentParams[1], &nStartTime)) {
	    throw std::runtime_error(strprintf("Invalid nStartTime (%s)", vDeploymentParams[1]));
	}
	if (!ParseInt64(vDeploymentParams[2], &nTimeout)) {
	    throw std::runtime_error(strprintf("Invalid nTimeout (%s)", vDeploymentParams[2]));
	}
	if (vDeploymentParams.size() > 3 && !ParseInt64(vDeploymentParams[3], &nStartHeight)) {
	    throw std::runtime_error(strprintf("Invalid nStartHeight (%s)", vDeploymentParams[3]));
	}
	if (vDeploymentParams.size() > 4 && !ParseInt64(vDeploymentParams[4], &nTimeoutHeight)) {
	    throw std::runtime_error(strprintf("Invalid nTimeoutHeight (%s)", vDeploymentParams[4]));
	}
	bool found = false;
	for (int j=0; j < (int)Consensus::MAX_VERSION_BITS_DEPLOYMENTS; ++j) {
	    if (vDeploymentParams[0] == VersionBitsDeploymentInfo[j].name) {
		UpdateVersionBitsParameters(Consensus::DeploymentPos(j), nStartTime, nTimeout, nStartHeight, nTimeoutHeight);
		found = true;
		LogPrintf("Setting version bits activation parameters for %s to start=%ld, timeout=%ld, start_height=%d, timeout_height=%d\n", vDeploymentParams[0], nStartTime, nTimeout, nStartHeight, nTimeoutHeight);
		break;
	    }
	}
	if (!found) {
	    throw std::runtime_error(strprintf("Invalid deployment (%s)", vDeploymentParams[0]));
	}
    }
}

static std::unique_ptr<const CChainParams> globalChainParams;

const CChainParams &Params() {
    assert(globalChainParams);
    return *globalChainParams;
}

std::unique_ptr<const CChainParams> CreateChainParams(const ArgsManager& args, const std::string& chain)
{
    if (chain == CBaseChainParams::MAIN) {
	return std::unique_ptr<CChainParams>(new CMainParams());
    } else if (chain == CBaseChainParams::TESTNET) {
	return std::unique_ptr<CChainParams>(new CTestNetParams());
    } else if (chain == CBaseChainParams::SIGNET) {
	return std::unique_ptr<CChainParams>(new CTestNetParams()); // TODO: Support SigNet
    } else if (chain == CBaseChainParams::REGTEST) {
	return std::unique_ptr<CChainParams>(new CRegTestParams(args));
    }
    throw std::runtime_error(strprintf("%s: Unknown chain %s.", __func__, chain));
}

void SelectParams(const std::string& network)
{
    SelectBaseParams(network);
    globalChainParams = CreateChainParams(gArgs, network);
}
