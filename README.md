# Tranche

[![Bitcoin-only](https://img.shields.io/badge/bitcoin-only-FF9900?logo=bitcoin)](https://twentyone.world)
[![LN](https://img.shields.io/badge/lightning-792EE5?logo=lightning)](https://mempool.space/lightning)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![Tranche Banner](static/tranche-banner.svg)](static/tranche-banner.svg)

## Prerequisites

* python (3.8+)
* pip
* docker

## Getting started

You can use `tranche` simply by installing via `pip` on your Terminal.

```sh
$ pip install tranche
> ...
> Installing collected packages: tranche
> Successfully installed tranche-0.2.1
$ tranche cluster
> Deploy specified local cluster:     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
> Generate addresses:                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
> Mine initial capital for parties:   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

You will have docker containers running in the backend, ready to be interfaced by your local
environment applications you are developing.

## Begin local mining

In order to properly test many functionalities, you will need to send mining commands to local
setup. You can achieve completely local and running environment with the following command:

```sh
$ tranche mine
╭───────── bitcoind ─────────╮╭────────────────────── 'lightning' (70 x 17) ───────────────────────╮
│ {                          ││                                                                    │
│   "blocks": 202,           ││                                                                    │
│   "chain": "regtest",      ││                                                                    │
│   "size_on_disk": 60548,   ││                                                                    │
│   "time": 1701427982       ││                                                                    │
│ }                          ││                                                                    │
│                            ││                                                                    │
│                            ││                 Layout(name='lightning', size=70)                  │
│                            ││                                                                    │
│                            ││                                                                    │
│                            ││                                                                    │
│                            ││                                                                    │
│                            ││                                                                    │
│                            ││                                                                    │
│                            ││                                                                    │
╰────────────────────────────╯╰────────────────────────────────────────────────────────────────────╯
```

## Cleanup

```sh
$ tranche clean                                                                                                                                                                             > 
> Remove active containers:           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

### Known issues
```python
docker.errors.DockerException: Error while fetching server API version: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))
```

See the following issue for Mac OSX troubleshooting.

[docker from_env and pull is broken on mac](https://github.com/docker/docker-py/issues/3059#issuecomment-1294369344)

Recommneded fix is to run the following command:

```sh
sudo ln -s "$HOME/.docker/run/docker.sock" /var/run/docker.sock
```

## License

This project is licensed under the terms of the MIT license.