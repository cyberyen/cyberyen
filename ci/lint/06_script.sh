#!/usr/bin/env bash
#
# Copyright (c) 2018-2019 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

export LC_ALL=C

# GitHub Actions sets GITHUB_EVENT_NAME / GITHUB_BASE_REF on pull_request.
# Preserve commit-script-check for PRs; skip when not a PR (same as the old
# Travis else-path).
if [ "${GITHUB_EVENT_NAME}" = "pull_request" ] && [ -n "${GITHUB_BASE_REF}" ]; then
  COMMIT_RANGE="origin/${GITHUB_BASE_REF}..HEAD"
  test/lint/commit-script-check.sh $COMMIT_RANGE
fi

test/lint/git-subtree-check.sh src/crypto/ctaes
test/lint/git-subtree-check.sh src/secp256k1-zkp
test/lint/git-subtree-check.sh src/univalue
test/lint/git-subtree-check.sh src/leveldb
test/lint/git-subtree-check.sh src/crc32c
test/lint/check-doc.py
test/lint/check-rpc-mappings.py .
test/lint/lint-all.sh
