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
> Successfully installed tranche-0.2.2
$ tranche cluster
> Deploy specified local cluster:            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:01
> Generate addresses:                        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
> Mine initial capital for parties:          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

You will have docker containers running in the backend, ready to be interfaced by your local
environment applications you are developing.

## Begin local mining

In order to properly test many functionalities, you will need to send mining commands to local
setup. You can achieve completely local and running environment with the following command:

```sh
$ tranche mine
> ╭───── containers ─────╮┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
> │ tranche-redis        │┃ Name          ┃ Nodekey      ┃ Channels  ┃ Peers  ┃ Height ┃ Synced? ┃
> │ tranche-postgres     │┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
> │ tranche-pong         ││ tranche-pong  │ 02fabeeaa9d  │ 2         │ 1      │ 216    │    true │
> │ tranche-ping         ││               │ 3da33d3eb12  │           │        │        │         │
> │ tranche-bitcoind     ││               │ 262e039d9b2  │           │        │        │         │
> │                      ││               │ 9d591f1b897  │           │        │        │         │
> │                      ││               │ c0ae6b158d0  │           │        │        │         │
> │                      ││               │ 5410d97efbc  │           │        │        │         │
> │                      │├───────────────┼──────────────┼───────────┼────────┼────────┼─────────┤
> │                      ││ tranche-ping  │ 02ac17a8d64  │ 2         │ 1      │ 216    │    true │
> │                      ││               │ 4194459b8f3  │           │        │        │         │
> │                      ││               │ deacf4e1a64  │           │        │        │         │
> │                      ││               │ 0fcbcdf9fbf  │           │        │        │         │
> │                      ││               │ 39e8423dfdc  │           │        │        │         │
> │                      ││               │ 3ffa2f7367f  │           │        │        │         │
> │                      │└───────────────┴──────────────┴───────────┴────────┴────────┴─────────┘
> │                      │╭──────────────────────────────────────────────────────────────────────╮
> │                      ││ Chain: regtest  Blocks: 216     Size: 65259     Time: 1701528030     │
> ╰──────────────────────╯╰──────────────────────────────────────────────────────────────────────╯
```

## Cleanup

```sh
$ tranche clean                                                                                                                                                                             > 
> Remove active containers:                  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:01
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