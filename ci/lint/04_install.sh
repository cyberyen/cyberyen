#!/usr/bin/env bash
#
# Copyright (c) 2018-2019 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

export LC_ALL=C

# Local stand-in for Travis's injected travis_retry (undefined outside Travis).
travis_retry() {
  local n=0
  local max=3
  until "$@"; do
    n=$((n + 1))
    if [ "$n" -ge "$max" ]; then
      return 1
    fi
    echo "travis_retry: attempt $n failed; retrying..." >&2
    sleep 1
  done
}

travis_retry pip3 install codespell==1.17.1
travis_retry pip3 install flake8==3.8.3
travis_retry pip3 install yq
travis_retry pip3 install mypy==0.971

SHELLCHECK_VERSION=v0.7.1
curl -sL "https://github.com/koalaman/shellcheck/releases/download/${SHELLCHECK_VERSION}/shellcheck-${SHELLCHECK_VERSION}.linux.x86_64.tar.xz" | tar --xz -xf - --directory /tmp/
export PATH="/tmp/shellcheck-${SHELLCHECK_VERSION}:${PATH}"
