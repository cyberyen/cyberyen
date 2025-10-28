Cyberyen Core version 0.21.5 is now available from:

 <https://github.com/cyberyen/cyberyen/releases/tag/v0.21.5>.

This is a new patch version release that includes, new features and important security updates.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/cyberyen/cyberyen/issues>

Notable changes
===============

AuxPoW Implementation
--------------------------

- `c4a62a5`: Implement auxpow correctly, based around original namecoin-implementation modified for PoW.
- `c64a813`: hard fork at 1265000 block height, AuxPow chainID from 16 to 4096 (0x1000)

Bug fixes
---------

- `d2aa236`: add MWEB view keys to dumpwallet
- `e368ec6`: don't include MWEB transactions if the input and output commitments in the block would sum to zero
- `66f49d2`: update seeds
- `8a682fd`: remove unused fSimplifiedRewards logic in GetBlockSubsidy
- `e205f95`: fix seeds

Credits
=======

Thanks to everyone who directly contributed to this release:

- [The Litecoin Core Developers](https://github.com/litecoin-project/litecoin/tree/master/doc/release-notes)
- [Barrystyle](https://github.com/barrystyle)
