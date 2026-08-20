#!/usr/bin/env bash
#
# Copyright (c) 2019-2020 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

export LC_ALL=C.UTF-8

export CONTAINER_NAME=ci_native_jammy
export DOCKER_NAME_TAG=ubuntu:22.04
export PACKAGES="python3-zmq python3-pip libevent-dev bsdmainutils libboost-filesystem-dev libboost-test-dev libboost-thread-dev libdb5.3++-dev libminiupnpc-dev libzmq3-dev libsqlite3-dev libssl-dev pkg-config iproute2"
export DEP_OPTS="NO_QT=1 NO_UPNP=1"
export GOAL="install"
export TEST_RUNNER_EXTRA="--timeout-factor=2"
export BITCOIN_CONFIG="--enable-zmq --with-incompatible-bdb --with-gui=no --with-sqlite --disable-bench"
export RUN_UNIT_TESTS_SEQUENTIAL=true
export RUN_UNIT_TESTS=${RUN_UNIT_TESTS:-true}
export RUN_FUNCTIONAL_TESTS=${RUN_FUNCTIONAL_TESTS:-true}
