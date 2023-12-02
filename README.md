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
╭──────── containers ────────╮┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
│ tranche-redis              │┃ Name          ┃ Nodekey      ┃ Channels ┃ Peers ┃ Height ┃ Synced? ┃
│ tranche-postgres           │┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│ tranche-pong               ││ tranche-pong  │ 0347db74eb8  │ 2        │ 1     │ 226    │    true │
│ tranche-ping               ││               │ 9d907d12e37  │          │       │        │         │
│ tranche-bitcoind           ││               │ 97d9dba4a44  │          │       │        │         │
│                            ││               │ 75eae124d94  │          │       │        │         │
│                            ││               │ 229d7c6470b  │          │       │        │         │
│                            ││               │ c5cbb59b34a  │          │       │        │         │
│                            │├───────────────┼──────────────┼──────────┼───────┼────────┼─────────┤
│                            ││ tranche-ping  │ 02b1154a16c  │ 2        │ 1     │ 226    │    true │
│                            ││               │ 3e084bb80e1  │          │       │        │         │
│                            ││               │ a2aa5b3c302  │          │       │        │         │
│                            ││               │ 13a183497e3  │          │       │        │         │
│                            ││               │ 62a96f76ff8  │          │       │        │         │
│                            ││               │ b8d4493e722  │          │       │        │         │
│                            │└───────────────┴──────────────┴──────────┴───────┴────────┴─────────┘
│                            │╭────────────────────────────────────────────────────────────────────╮
│                            ││ Chain: regtest  Blocks: 226     Size: 68248     Time: 1701525985   │
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