Cyberyen Core version 0.21.6 is now available from:

 <https://github.com/cyberyen/cyberyen/releases/tag/v0.21.6.1>.

This release includes important security updates. All node operators and wallet users are strongly encouraged to upgrade ASAP.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/cyberyen/cyberyen/issues>

Notable changes
===============

Important MWEB updates
----------------------

This release contains important MWEB validation and state-handling fixes.
Upgrading is recommended for all users, especially miners, pools, and node
operators using MWEB.

- Added additional validation for MWEB inputs, pegins, HogEx data, kernel fees,
  and kernel lock heights (`4b12c49`, `27ab3c9`, `9628e5e`, `857acb1`,
  `81978d9`, `cb2991c`).
- Hardened MWEB amount and fee calculations against overflow and invalid edge
  cases (`27ab3c9`, `e7ef75d`).
- Added fallback handling for rare hash-to-secret-key cases so derived MWEB
  keys are valid scalars (`b732a2d`).
- Updated MWEB chainstate during block replay and crash recovery (`9ae6f4f`).

Network and policy changes
--------------------------

- Increased the maximum P2P protocol message length to 32 MB so valid MWEB
  blocks and messages fit under the message-size limit (`c12979e`).
- Enforced standard script policy checks for pegout scripts (`f71feab`).

Mining changes
--------------

- Avoid reading the previous block from disk when constructing HogEx
  transactions; use MWEB data already stored in the block index (`b27766d`).
- Improved `getblocktemplate` fee and sigop accounting for transactions carrying
  MWEB data (`b27766d`).
- Avoid including MWEB transactions in candidate blocks when their input and
  output commitments would sum to zero (`e368ec6`).

Wallet and RPC changes
----------------------

- Fixed MWEB balance and pegout accounting (`0eee8ee`).
- Added MWEB view keys to `dumpwallet` (`d2aa236`).
- Supported `maxfeerate=0` for MWEB transactions in `sendrawtransaction` and
  `testmempoolaccept` (`689c97f`).

Bug fixes
---------

- Fixed MWEB PMMR rewind corruption and improved MMR file write durability
  (`0cbfba9`, `3824999`, `452c9da`).
- Fixed a cache leaf bounds check (`f699f1e`).
- Fixed a transaction index consistency issue that could occur if writing block
  data failed after the index commit (`f61cde6`).
- Fixed wallet loading with Boost 1.78 and newer (`7981eca`, `a7dfb41`).

Build and test changes
----------------------

- Added missing `<cstdint>` includes needed by some compilers (`bda8753`).
- Replaced the functional test dependency on the external `litecoin_scrypt`
  Python package (`d2aa236`).
- Added and expanded tests for MWEB P2P messages, duplicate pegins, crash
  recovery, mutated blocks, mining, and wallet/RPC behavior.
- Normalized line endings in selected documentation, Qt resources, and fuzz test
  files (`9981821`).

Credits
=======

Thanks to everyone who directly contributed to this release:

- [David Burkett](https://github.com/DavidBurkett/)
- [Loshan](https://github.com/losh11)
