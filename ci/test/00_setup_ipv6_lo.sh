#!/usr/bin/env bash
# Ensure local IPv6 is usable for functional tests that bind/proxy on ::1.
#
# Docker often has disable_ipv6=0 and ::1 on lo, but glibc getaddrinfo with
# AI_ADDRCONFIG (bitcoind default -dns) still rejects ::1 unless a non-host
# IPv6 address exists on an interface. feature_proxy / rpc_bind --ipv6 need that.
export LC_ALL=C
set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  exit 0
fi

if ! command -v ip >/dev/null 2>&1; then
  exit 0
fi

# Clear disable_ipv6 on all interfaces (all/default/lo and others).
if [[ -d /proc/sys/net/ipv6/conf ]]; then
  for iface in /proc/sys/net/ipv6/conf/*; do
    if [[ -w "$iface/disable_ipv6" ]]; then
      echo 0 > "$iface/disable_ipv6" || true
    fi
  done
fi

# Always put a non-host address on lo.
ip -6 addr replace fd00:dead:beef::1/64 dev lo || true

# Also add an address on the first up non-lo interface (eth*/ens*/enp*).
dev=$(ip -o link show up | awk -F': ' '$2 !~ /^lo/ { sub(/@.*/, "", $2); print $2; exit }' || true)
if [[ -n "${dev:-}" ]]; then
  ip -6 addr replace fd00:c0ff:ee::1/64 dev "$dev" || true
fi

exit 0
