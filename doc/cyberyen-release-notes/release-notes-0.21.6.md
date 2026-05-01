0.21.6 Release Notes
====================

Cyberyen Core version 0.21.6 is now available from:

 <https://github.com/cyberyen/cyberyen/releases/tag/v0.21.6>.

This release includes important security updates. All node operators and wallet users are strongly encouraged to upgrade ASAP.

Please report bugs using the issue tracker at GitHub:

 <https://github.com/cyberyen/cyberyen/issues>

Notable changes
===============

Important Security Updates
--------------------------

This release contains fixes for the following security issues:

- `4b12c49`: Belt-and-suspenders input commitment and public key checks on MWEB inputs, providing additional defense-in-depth
during MWEB transaction validation
This corrects MWEB input/output accounting going forward and is a required upgrade for all node operators, miners, and wallet users
- `27ab3c9`: Prevent kernel fee overflow during MWEB transaction validation
- `a3846b4`: Erase block data for mutated blocks to avoid miner DoS

MWEB stability and durability fixes
-----------------------------------

- `0cbfba9`: fix data corruption issue on PMMR rewind
- `3824999`, `452c9da`: improve file write durability for MMRs

Wallet
------

- `d2aa236`: add MWEB view keys to `dumpwallet` output
- `7981eca`, `a7dfb41`: fix wallet with Boost library >= 1.78
- `0eee8ee`: wallet: quick pegout accounting fix

RPC and indexing
----------------

- `47215a7`: allow `getblocktemplate` for test chains when unconnected or in IBD

Build changes
-------------

- `38c6ef8`: add missing `<cstdint>` include

Test related fixes
------------------

- `f48b3ad`: functional test framework fix
- `cdb4859`: functional test demonstrating handling of mutated blocks

Credits
=======

Thanks to everyone who directly contributed to this release:

- [The Bitcoin Core Developers](https://github.com/bitcoin/bitcoin/)
- [David Burkett](https://github.com/DavidBurkett/)
- [Hector Chu](https://github.com/hectorchu)
- [Loshan](https://github.com/losh11)
- [Luke E. McKay](https://github.com/luke-mckay)
- [Soren Stoutner](https://github.com/sorenstoutner)
- [Jorge Maldonado Ventura](https://github.com/jorgesumle)
- [yujianxian](https://github.com/yujianxian)
- [AlexRadik](https://github.com/AleksandrRadik)
