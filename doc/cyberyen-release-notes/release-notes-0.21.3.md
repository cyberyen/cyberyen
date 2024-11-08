Cyberyen Core version 0.21.3 is now available from:

 <https://github.com/cyberyen/cyberyen/releases/tag/v0.21.3>.

This is a new patch version release that includes, new features and important security updates.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/cyberyen/cyberyen/issues>

Notable changes
===============

Important Security Updates
--------------------------

This release contains fixes for the following security vulnerabilities:

- [CVE-2024-35202](https://www.cvedetails.com/cve/CVE-2024-35202/),
which allows remote attackers to cause a denial of service (blocktxn message-handling assertion and node exit)
by including transactions in a blocktxn message that are not committed to in a block's merkle root.
FillBlock can be called twice for one PartiallyDownloadedBlock instance.
  - `c4ad41f`: backported from Bitcoin Core (`a8897f6`)

- [Hindered block propagation due to mutated blocks](https://bitcoincore.org/en/2024/10/08/disclose-mutated-blocks-hindering-propagation/),
where a peer could send mutated blocks which could clear the download state of other peers that also announced block, hindering block propagation.
  - `aaa5b54`: backported from Bitcoin Core (`dbfc748`)

- [Infinite loop bug in miniupnp dependency](https://bitcoincore.org/en/2024/07/31/disclose-upnp-oom/),
which could be exploited by an attacker on the local network to trigger an OOM.
  - `f5c3008`: backported from Bitcoin Core (`fa2a5b8`)

Bug fixes
---------
- `9a297f7`: default -peerblockfilters and -blockfilterindex to off when pruning is enabled

Test related fixes
------------------
- `368564a`: fix functional tests

Credits
=======

Thanks to everyone who directly contributed to this release:

- [The Bitcoin Core Developers](https://github.com/bitcoin/bitcoin/tree/master/doc/release-notes)
- [The Litecoin Core Developers](https://github.com/litecoin-project/litecoin/tree/master/doc/release-notes)
