Cyberyen Core version 0.21.2.2 is now available from:

 <https://download.cyberyen.org/cyberyen-0.21.2.3/>.

This is a new patch version release that includes important security updates. Fix block subsidy calculations.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/cyberyen/cyberyen/issues>

To receive security and update notifications, please subscribe to:

  <https://matrix.to/#/#cyberyen-dev:matrix.org>

Notable changes
===============

Important Security Updates
--------------------------

This release contains fixes that harden node and network security. These fixes are very important for every node operator and wallet user.

This protects nodes on lower end hardware to not run out of memory in the face of increased network activity.

Fix Block Subsidy Calculations
---------------

* New-style constant rewards for each halving interval.
* Constant inflation. Reward at 600k+ is constant 10 000 COINS


Credits
=======

Thanks to everyone who directly contributed to this release:

- [The Bitcoin Core Developers](https://github.com/bitcoin/bitcoin/tree/master/doc/release-notes)
- [The Litecoin Core Developers](https://github.com/litecoin-project/litecoin/tree/master/doc/release-notes)
- [teh Cyberyen Core](https://github.com/cyberyen/cyberyen/tree/master/doc/release-notes)
