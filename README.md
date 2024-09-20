Cyberyen Core integration/staging tree
======================================

https://cyberyen.org

Cyberyen Core is an open-source software application that allows users to operate a node within the Cyberyen peer-to-peer network. Utilizing the Scrypt hashing method for Proof of Work, the software facilitates the downloading and complete validation of blocks and transactions. It also includes an optional wallet and graphical user interface, enhancing the overall user experience.

Further information about Cyberyen Core is available in the [doc folder](/doc).

License
-------

Cyberyen Core is released under the terms of the MIT license. See [COPYING](COPYING) for more information or see [opensource.org](https://opensource.org/licenses/MIT)

Usage
-----

To begin using Cyberyen Core, please refer to the [installation guide](INSTALL.md) and the [getting started](doc/) tutorial.

The JSON-RPC API provided by Cyberyen Core is self-documenting and can be accessed using `cyberyen-cli help`. Detailed information for each command is available with `cyberyen-cli help <command>`. For additional reference, you may consult the [Bitcoin Core documentation](https://developer.bitcoin.org/reference/rpc/), which implements a similar protocol and offers a browsable version.

### Ports

Cyberyen Core by default uses port `58383` for peer-to-peer communication that is needed to synchronize the "mainnet" blockchain and stay informed of new transactions and blocks. Additionally, a JSONRPC port can be opened, which defaults to port `58382` for mainnet nodes. It is strongly recommended to not expose RPC ports to the public internet.

| Function | mainnet | testnet | regtest |
| :------- | ------: | ------: | ------: |
| P2P      |   58383 |   44551 |   18440 |
| RPC      |   58382 |   44550 |   18439 |

Contributing
------------

Cyberyen Core is an open source and community driven software. The development process is open and publicly visible; anyone can see, discuss and work on the software.

The `master` branch is regularly built (see `doc/build-*.md` for instructions) and tested, but it is not guaranteed to be completely stable. [Tags](https://github.com/cyberyen/cyberyen/tags) are created regularly from release branches to indicate new official, stable release versions of Cyberyen Core.

Please see [the contribution guide](CONTRIBUTING.md) to see how you can participate in the development of Cyberyen Core.

Communities
-----------

Join the Cyberyen communities on various social media platforms to stay informed, connect with others, discuss topics related to Cyberyen, and seek or offer assistance.

Here are some platforms to explore:
[Cyberyen [Matrix]](https://matrix.to/#/#cyberyen:matrix.org)
