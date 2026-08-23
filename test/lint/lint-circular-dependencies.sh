#!/usr/bin/env bash
#
# Copyright (c) 2018-2020 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#
# Check for circular dependencies

export LC_ALL=C

EXPECTED_CIRCULAR_DEPENDENCIES=(
    "auxpow -> primitives/block -> auxpow"
    "chainparams -> protocol -> chainparams"
    "chainparamsbase -> util/system -> chainparamsbase"
    "index/txindex -> validation -> index/txindex"
    "interfaces/chain.h -> node/context -> interfaces/chain.h"
    "interfaces/wallet.h -> wallet/txrecord -> wallet/wallet -> interfaces/wallet.h"
    "miner -> mweb/mweb_miner -> miner"
    "mweb/mweb_node -> validation -> mweb/mweb_node"
    "mweb/mweb_transact -> wallet/txassembler -> mweb/mweb_transact"
    "mweb/mweb_wallet -> wallet/wallet -> mweb/mweb_wallet"
    "policy/fees -> txmempool -> policy/fees"
    "policy/fees -> txmempool -> validation -> policy/fees"
    "qt/addresstablemodel -> qt/walletmodel -> qt/addresstablemodel"
    "qt/bitcoingui -> qt/walletframe -> qt/bitcoingui"
    "qt/recentrequeststablemodel -> qt/walletmodel -> qt/recentrequeststablemodel"
    "qt/sendcoinsdialog -> qt/walletmodel -> qt/sendcoinsdialog"
    "qt/transactiontablemodel -> qt/walletmodel -> qt/transactiontablemodel"
    "rpc/blockchain -> rpc/rawtransaction -> rpc/blockchain"
    "script/address -> script/standard -> script/address"
    "txmempool -> validation -> txmempool"
    "wallet/fees -> wallet/wallet -> wallet/fees"
    "wallet/reserve -> wallet/wallet -> wallet/reserve"
    "wallet/txassembler -> wallet/wallet -> wallet/txassembler"
    "wallet/wallet -> wallet/walletdb -> wallet/wallet"
)

EXIT_CODE=0

CIRCULAR_DEPENDENCIES=()

IFS=$'\n'
for CIRC in $(cd src && ../contrib/devtools/circular-dependencies.py {*,*/*,*/*/*}.{h,cpp} | sed -e 's/^Circular dependency: //'); do
    CIRCULAR_DEPENDENCIES+=( "$CIRC" )
    IS_EXPECTED_CIRC=0
    for EXPECTED_CIRC in "${EXPECTED_CIRCULAR_DEPENDENCIES[@]}"; do
        if [[ "${CIRC}" == "${EXPECTED_CIRC}" ]]; then
            IS_EXPECTED_CIRC=1
            break
        fi
    done
    if [[ ${IS_EXPECTED_CIRC} == 0 ]]; then
        echo "A new circular dependency in the form of \"${CIRC}\" appears to have been introduced."
        echo
        EXIT_CODE=1
    fi
done

for EXPECTED_CIRC in "${EXPECTED_CIRCULAR_DEPENDENCIES[@]}"; do
    IS_PRESENT_EXPECTED_CIRC=0
    for CIRC in "${CIRCULAR_DEPENDENCIES[@]}"; do
        if [[ "${CIRC}" == "${EXPECTED_CIRC}" ]]; then
            IS_PRESENT_EXPECTED_CIRC=1
            break
        fi
    done
    if [[ ${IS_PRESENT_EXPECTED_CIRC} == 0 ]]; then
        echo "Good job! The circular dependency \"${EXPECTED_CIRC}\" is no longer present."
        echo "Please remove it from EXPECTED_CIRCULAR_DEPENDENCIES in $0"
        echo "to make sure this circular dependency is not accidentally reintroduced."
        echo
        EXIT_CODE=1
    fi
done

exit ${EXIT_CODE}
