#!/usr/bin/env bash
# Ensure local IPv6 is usable for functional tests that bind/proxy on ::1.
#
# Docker often has disable_ipv6=0 and ::1 on lo, but glibc getaddrinfo with
# AI_ADDRCONFIG (bitcoind default -dns) still rejects ::1 unless a non-host
# IPv6 address exists on an interface. feature_proxy / rpc_bind --ipv6 need that.
set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  exit 0
fi

if [[ -w /proc/sys/net/ipv6/conf/all/disable_ipv6 ]]; then
  echo 0 > /proc/sys/net/ipv6/conf/all/disable_ipv6 || true
fi

if command -v ip >/dev/null 2>&1; then
  ip -6 addr replace fd00:dead:beef::1/64 dev lo || true
fi
