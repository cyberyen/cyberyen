// Copyright (c) 2024 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <blockencodings.h>
#include <chainparams.h>
#include <consensus/merkle.h>
#include <consensus/validation.h>
#include <primitives/block.h>
#include <primitives/transaction.h>
#include <sync.h>
#include <test/fuzz/FuzzedDataProvider.h>
#include <test/fuzz/fuzz.h>
#include <test/fuzz/util.h>
#include <txmempool.h>

#include <cassert>
#include <cstdint>
#include <limits>
#include <optional>
#include <set>
#include <utility>
#include <vector>

namespace {
PartiallyDownloadedBlock::CheckBlockFn FuzzedCheckBlock(std::optional<BlockValidationResult> result)
{
    return [result](const CBlock&, BlockValidationState& state, const Consensus::Params&, bool, bool) {
        if (result) {
            return state.Invalid(*result);
        }
        return true;
    };
}
} // namespace

void initialize()
{
    static const ECCVerifyHandle verify_handle;
    SelectParams(CBaseChainParams::REGTEST);
}

void test_one_input(const std::vector<uint8_t>& buffer)
{
    FuzzedDataProvider fuzzed_data_provider{buffer.data(), buffer.size()};

    auto block{ConsumeDeserializable<CBlock>(fuzzed_data_provider)};
    if (!block || block->vtx.empty() ||
        block->vtx.size() >= std::numeric_limits<uint16_t>::max()) {
        return;
    }

    CBlockHeaderAndShortTxIDs cmpctblock{*block, /*fUseWTXID=*/fuzzed_data_provider.ConsumeBool()};

    CTxMemPool pool;
    PartiallyDownloadedBlock pdb{&pool, cmpctblock.mweb_block};

    // Set of available transactions (mempool or extra_txn)
    std::set<uint16_t> available;
    // The coinbase is always available
    available.insert(0);

    std::vector<std::pair<uint256, CTransactionRef>> extra_txn;
    for (size_t i = 1; i < block->vtx.size(); ++i) {
        const CTransactionRef& tx{block->vtx[i]};

        const bool add_to_extra_txn{fuzzed_data_provider.ConsumeBool()};
        const bool add_to_mempool{fuzzed_data_provider.ConsumeBool()};

        if (add_to_extra_txn) {
            extra_txn.emplace_back(tx->GetWitnessHash(), tx);
            available.insert(static_cast<uint16_t>(i));
        }

        if (add_to_mempool) {
            LOCK2(cs_main, pool.cs);
            pool.addUnchecked(ConsumeTxMemPoolEntry(fuzzed_data_provider, *tx));
            available.insert(static_cast<uint16_t>(i));
        }
    }

    const ReadStatus init_status{pdb.InitData(cmpctblock, extra_txn)};

    std::vector<CTransactionRef> missing;
    // Whether we skipped a transaction that should be included in `missing`.
    // FillBlock should never return READ_STATUS_OK if that is the case.
    bool skipped_missing{false};
    for (size_t i = 0; i < cmpctblock.BlockTxCount(); ++i) {
        // If init_status == READ_STATUS_OK then an available transaction in the
        // compact block (i.e. IsTxAvailable(i) == true) implies that we marked
        // that transaction as available above (i.e. available.count(i) > 0).
        // The reverse is not true, due to possible compact block short id
        // collisions (i.e. available.count(i) > 0 does not imply
        // IsTxAvailable(i) == true).
        if (init_status == READ_STATUS_OK) {
            assert(!pdb.IsTxAvailable(i) || available.count(static_cast<uint16_t>(i)) > 0);
        }

        const bool skip{fuzzed_data_provider.ConsumeBool()};
        if (!pdb.IsTxAvailable(i) && !skip) {
            missing.push_back(block->vtx[i]);
        }

        skipped_missing |= (!pdb.IsTxAvailable(i) && skip);
    }

    // Mock CheckBlock
    const bool fail_check_block{fuzzed_data_provider.ConsumeBool()};
    const auto validation_result = fuzzed_data_provider.PickValueInArray({
        BlockValidationResult::BLOCK_RESULT_UNSET,
        BlockValidationResult::BLOCK_CONSENSUS,
        BlockValidationResult::BLOCK_RECENT_CONSENSUS_CHANGE,
        BlockValidationResult::BLOCK_CACHED_INVALID,
        BlockValidationResult::BLOCK_INVALID_HEADER,
        BlockValidationResult::BLOCK_MUTATED,
        BlockValidationResult::BLOCK_MISSING_PREV,
        BlockValidationResult::BLOCK_INVALID_PREV,
        BlockValidationResult::BLOCK_TIME_FUTURE,
        BlockValidationResult::BLOCK_CHECKPOINT,
    });
    pdb.m_check_block_mock = FuzzedCheckBlock(
        fail_check_block ? std::optional<BlockValidationResult>{validation_result} : std::nullopt);

    CBlock reconstructed_block;
    const ReadStatus fill_status{pdb.FillBlock(reconstructed_block, missing)};
    switch (fill_status) {
    case READ_STATUS_OK:
        assert(!skipped_missing);
        assert(!fail_check_block);
        assert(block->GetHash() == reconstructed_block.GetHash());
        break;
    case READ_STATUS_CHECKBLOCK_FAILED:
    case READ_STATUS_FAILED:
        assert(fail_check_block);
        break;
    case READ_STATUS_INVALID:
        break;
    }
}
