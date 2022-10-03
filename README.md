<div align="center">
<h1>
<img src="./cyberyen.svg" alt="Cyberyen" width="300"/>
<br/><br/>
CYBERYEN CORE
<br/>
[C¥]
<br/><br/>
The Dark Side of the Moon 🌚
</h1>
</div>

<br/>
<div align="center">
Cyberyen is a hybrid cryptocurrency grown from the Litecoin MWEB fork with grafted Dogecoin block parameters. The Cyberyen Core is the name of open source software that allows anyone to operate a node in the Cyberyen blockchain network and uses the Scrypt hashing method for Proof of Work adopted for this cryptocurrencies.

<br/><br/>
For more information, please see the website: <br/>https://cyberyen.org/
</div>

## Usage 🔗

To start your journey with Cyberyen Core, see the [installation guide](INSTALL.md) and the [getting started](doc/) tutorial.

The JSON-RPC API provided by Cyberyen Core is self-documenting and can be browsed with `cyberyen-cli help`, while detailed information for each command can be viewed with `cyberyen-cli help <command>`. Alternatively, see the [Bitcoin Core documentation](https://developer.bitcoin.org/reference/rpc/) - which implement a similar protocol - to get a browsable version.

### Ports

Cyberyen Core by default uses port `58383` for peer-to-peer communication that
is needed to synchronize the "mainnet" blockchain and stay informed of new
transactions and blocks. Additionally, a JSONRPC port can be opened, which
defaults to port `58382` for mainnet nodes. It is strongly recommended to not
expose RPC ports to the public internet.

| Function | mainnet | testnet | regtest |
| :------- | ------: | ------: | ------: |
| P2P      |   58383 |   44551 |   18440 |
| RPC      |   58382 |   44550 |   18439 |

## Contributing 🦾

Cyberyen Core is an open source and community driven software. The development process is open and publicly visible; anyone can see, discuss and work on the software.

The `master` branch is regularly built (see `doc/build-*.md` for instructions) and tested, but it is not guaranteed to be
completely stable. [Tags](https://github.com/cyberyen/cyberyen/tags) are created regularly from release branches to indicate new official, stable release versions of Cyberyen Core.

Please see [the contribution guide](CONTRIBUTING.md) to see how you can participate in the development of Cyberyen Core.

## Communities 👽🪐

You can join the communities on different social media.
To see what's going on, meet people & discuss, learn
about Cyberyen, give or ask for help, to share your project.

Here are some places to visit:
[Cyberyen [Matrix]](https://matrix.to/#/#cyberyen:matrix.org)

## License 📄
Cyberyen Core is released under the terms of the MIT license. See
[COPYING](COPYING) for more information or see
[opensource.org](https://opensource.org/licenses/MIT)
