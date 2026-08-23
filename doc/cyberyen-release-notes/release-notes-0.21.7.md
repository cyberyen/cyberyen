0.21.7 Release Notes
====================

Cyberyen Core version 0.21.7 is now available from:

 <https://github.com/cyberyen/cyberyen/releases/tag/v0.21.7>.

This release ports the MWEB hardening set from Litecoin Core 0.21.5.6,
restores a protection that was absent from 0.21.6.1, fixes a node abort on
-reindex, repairs the test suite, and fixes build and CI packaging so the
release can be built and verified from the source tarball.

There are no mainnet consensus rule changes in this release.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/cyberyen/cyberyen/issues>

Notable changes
===============

MWEB hardening (ported from Litecoin Core 0.21.5.6)
---------------------------------------------------

- Kernels signalling a pegout with no pegouts are non-standard.
- Outputs with a malformed Ke or Ko public key are non-standard; wallet
  scanning no longer aborts on them.
- Block assembly enforces the MWEB input limit.
- Relay policy bounds MWEB transaction weight and input count before the
  expensive signature and rangeproof verification.
- MWEB leafset and UTXO serving is rate-limited node-wide, so the limit
  survives a peer reconnecting.
- Peers delivering a mutated MWEB body in a compact block are discouraged.
- A block whose mutated serialization is discarded keeps its validated
  transaction metadata, so already-downloaded descendants stay linked.

Restored protection
-------------------

- CoinsViewCache::ApplyBlock again applies a block to a temporary cache and
  flushes only on success. This upstream protection was ported correctly in
  0.21.6, then removed in a build fix while dropping an unused parameter, and
  is therefore absent from 0.21.6.1.

Node fixes
----------

- Fixed an abort on -reindex. Cyberyen buries CSV and BIP34 at height 0 on all
  networks, so the genesis block reached branches that upstream never reaches
  at height 0, tripping an assertion. The genesis guard is now explicit, as it
  already was in ConnectBlock and AcceptBlockHeader.
- fPowNoRetargeting is honored in GetNextWorkRequired. It was unreachable
  because the KGW/DGW/LWMA dispatch returns before the branch that checked it.
  Affects regtest only; mainnet and testnet4 set the flag false.

Build and CI
------------

- Fix Boost 1.70 build on glibc >= 2.34 in depends (pthread stack minimum
  guard in Boost.Thread).
- Ship libmw headers and blake3 sources in the source distribution; blake3 is
  compiled into Hasher.cpp via #include, not as separate objects, so
  libbitcoinconsensus links without duplicate symbols.
- CI installs cmake so depends can build libfmt.
- Lint: shellcheck fixes, codespell excludes for vendored trees.
- bitcoin-util-test fixtures use Cyberyen base58 prefixes and expected JSON.
- test_runner.py treats cyberyen_scrypt.py as a framework helper, not a
  missing functional test script.

Testing
-------

- Regtest activates MWEB by height (window 144/288, active at 432), matching
  what the test framework already documented. Auxpow block versions cannot
  carry BIP9 signalling bits, so the time-based path could never activate.
- Test fixtures inherited from Bitcoin and Litecoin now use Cyberyen
  parameters: WIF prefix 156, cymweb and rcy address encodings with recomputed
  checksums, block subsidy, genesis timestamp, and network magic.
- mweb_reorg forces a canonical transparent→MWEB pegin so the test does not
  degenerate into MWEB→MWEB under Cyberyen's block subsidy.
- The unit binary exits cleanly; libmw Test* suites pass.
- GitHub Actions on Ubuntu 22.04 (lint and native-jammy: build from
  distdir, unit tests, functional tests) passes on this release branch.
- p2p_dos_header_tree remains skipped because there is still no mechanism to
  set a non-genesis regtest checkpoint.

Downgrade note
--------------

This release persists a new block-index status bit,
BLOCK_DISCARDED_MUTATED_DATA (bit 29 of CBlockIndex::nStatus), set when a
mutated MWEB block's serialization is discarded while its validated
transaction metadata is kept. An older node reading such an index sees
nTx > 0 with BLOCK_HAVE_DATA clear, which violates the equivalence its
CheckBlockIndex asserts. That check does not run by default on mainnet or
testnet4; it runs on regtest, and anywhere -checkblockindex is passed. In
those cases an older node can abort at startup. Recovery is to return to this
version: an older node cannot reindex out of it, because the -reindex abort at
genesis is fixed only here.

Not included
------------

- MWEB output freezing. Cyberyen was not attacked and has never carried the
  frozen-output rules Litecoin adopted; this release does not introduce them.
- The consensus rule rejecting empty MWEB pegout features. Only the relay
  policy form is included; the consensus form needs its own activation height.
- Signet. -chain=signet still maps to testnet4.
- A mechanism to set a non-genesis regtest checkpoint, so
  p2p_dos_header_tree remains skipped with that reason recorded.
