#!/usr/bin/env bash
#
# Copyright (c) 2019-2020 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

export LC_ALL=C.UTF-8

export CONTAINER_NAME=ci_native_nowallet
export DOCKER_NAME_TAG=ubuntu:22.04
export PACKAGES="python3-zmq python3-pip libevent-dev bsdmainutils libboost-filesystem-dev libboost-test-dev libboost-thread-dev libminiupnpc-dev libssl-dev pkg-config"
export DEP_OPTS="NO_WALLET=1 NO_QT=1"
export GOAL="install"
export BITCOIN_CONFIG="--disable-wallet --with-gui=no --disable-bench"
