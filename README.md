# Aesir

[![Bitcoin-only](https://img.shields.io/badge/bitcoin-only-FF9900?logo=bitcoin)](https://twentyone.world)
[![LN](https://img.shields.io/badge/lightning-792EE5?logo=lightning)](https://mempool.space/lightning)
[![Docker](https://img.shields.io/badge/docker-2496ED?&logo=docker&logoColor=white)](https://hub.docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Top](https://img.shields.io/github/languages/top/krutt/aesir)](.)
[![Languages](https://img.shields.io/github/languages/count/krutt/aesir)](.)
[![Size](https://img.shields.io/github/repo-size/krutt/aesir)](.)
[![Last commit](https://img.shields.io/github/last-commit/krutt/aesir/master)](.)

[![Aesir Banner](static/aesir-banner.svg)](static/aesir-banner.svg)

## Prerequisites

* python (3.8+)
* pip
* docker

## Getting started

You can use `aesir` simply by installing via `pip` on your Terminal.

```sh
pip install aesir
```

And then you can begin deploying local cluster as such:

```sh
aesir deploy
```

The initial deployment may take some time at pulling required images from their respective
repositories. Results may lock as such:

```sh
$ pip install aesir
> ...
> Installing collected packages: aesir
> Successfully installed aesir-0.2.5
$ aesir deploy
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
$ aesir mine
> ╭───── containers ─────╮┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
> │ aesir-redis        │┃ Name          ┃ Nodekey      ┃ Channels  ┃ Peers  ┃ Height ┃ Synced? ┃
> │ aesir-postgres     │┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
> │ aesir-pong         ││ aesir-pong  │ 02fabeeaa9d  │ 2         │ 1      │ 216    │    true │
> │ aesir-ping         ││               │ 3da33d3eb12  │           │        │        │         │
> │ aesir-bitcoind     ││               │ 262e039d9b2  │           │        │        │         │
> │                      ││               │ 9d591f1b897  │           │        │        │         │
> │                      ││               │ c0ae6b158d0  │           │        │        │         │
> │                      ││               │ 5410d97efbc  │           │        │        │         │
> │                      │├───────────────┼──────────────┼───────────┼────────┼────────┼─────────┤
> │                      ││ aesir-ping  │ 02ac17a8d64  │ 2         │ 1      │ 216    │    true │
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

### Cluster types

Currently there are two supported cluster-types in this project. Specified by flags,
`--duo` (default), or `--uno` with the following set-up:

| Type | Description                                                                |
| ---- | -------------------------------------------------------------------------- |
|  duo | Contains two LND nodes named `aesir-ping` and `aesir-pong` unified by <br> one single `aesir-bitcoind` service. 
|  uno | Only has one LND node named `aesir-lnd` connected to `aesir-bitcoind`. |

### Peripheral containers

This project also helps you setup peripheral services to make development process easier, too.
For example, if you want to deploy a duo-cluster with attached postgres database, run the following:

```sh
$ aesir deploy --postgres
> ...
$ aesir mine
> ╭───── containers ─────╮┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
> │ aesir-postgres       │┃ Name          ┃ Nodekey      ┃ Channels  ┃ Peers  ┃ Height ┃ Synced? ┃
> │ aesir-pong           │┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
> │ aesir-ping           ││ aesir-pong    │ 3da33d3eb12  │ 2         │ 1      │ 216    │    true │
> │ aesir-bitcoind       ││               │ deacf4e1a64  │           │        │        │         │
> │ ...                  ││ ...           │ ...          │ ...       │ ...    │ ...    │ ...     │
```

Or run an uno-cluster with both attached postgres database and redis solid store cache like this:

```sh
$ aesir deploy --uno --postgres --redis
> ...
$ aesir mine
> ╭───── containers ─────╮┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
> │ aesir-postgres       │┃ Name          ┃ Nodekey      ┃ Channels  ┃ Peers  ┃ Height ┃ Synced? ┃
> │ aesir-redis          │┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
> │ aesir-lnd            ││ aesir-lnd     │ c0ae6b158d0  │ 0         │ 0      │ 202    │    true │
> │ aesir-bitcoind       ││               │ 4194459b8f3  │           │        │        │         │
> │ ...                  ││ ...           │ ...          │ ...       │ ...    │ ...    │ ...     │
```

## Cleanup

Use the following command to clean up active `aesir-*` containers:

```sh
aesir clean
```

🚧  This will resets the current test state, so use with care. Example below:

```sh
$ aesir clean
> Remove active containers:                  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:01
```

## Roadmap

* Add `aesir-lnd-krub` peripheral service using [lnd-krub](https://github.com/krutt/lnd-krub)
* Add `aesir-tesla-ball` peripheral service using [tesla-ball](https://github.com/krutt/tesla-ball)
* Write [click](https://click.palletsprojects.com) tests.
* Make image versioning a little bit more intuitive.
* Add `aesir-ord` peripheral service using [ord](https://github.com/ordinals/ord)
* Add `aesir-bitvm` peripheral service using [BitVM](https://github.com/BitVM/BitVM)
* Create and add some type of `ordapi` peripheral service.
* Implement dashboard walkthrough a la [kylepollina/objexplore](https://github.com/kylepollina/objexplore)

## Contributions

This project uses [poetry](https://python-poetry.org) package manager to keep track of dependencies.
You can set up your local environment as such:

```sh
pip install --user poetry
```

And then you can install development dependencies like so:

```sh
$ pip install --user poetry
> ...
$ poetry install --with dev  # install with development dependencies
> Installing dependencies from lock file
>
> Package operations: 33 installs, 0 updates, 0 removals
>
>   • ...
>   • ...
>   • ...
>   • ...
>
> Installing the current project: aesir (0.2.5)
```

### Known issues

You may run into this setback when first running this project. This is a
[docker-py](https://github.com/docker/docker-py/issues/3059) issue widely known as of October 2022.

```python
docker.errors.DockerException:
  Error while fetching server API version: (
    'Connection aborted.', FileNotFoundError(
      2, 'No such file or directory'
    )
  )
```

See the following issue for Mac OSX troubleshooting.
[docker from_env and pull is broken on mac](https://github.com/docker/docker-py/issues/3059#issuecomment-1294369344)
Recommended fix is to run the following command:

```sh
sudo ln -s "$HOME/.docker/run/docker.sock" /var/run/docker.sock
```

## License

This project is licensed under the terms of the MIT license.