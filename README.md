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
pip install tranche
```

And then you can begin deploying local cluster as such:

```sh
tranche deploy
```

The initial deployment may take some time at pulling required images from their respective
repositories. Results may lock as such:

```sh
$ pip install tranche
> ...
> Installing collected packages: tranche
> Successfully installed tranche-0.2.5
$ tranche deploy
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

### Cluster types

Currently there are two supported cluster-types in this project. Specified by flags,
`--duo` (default), or `--uno` with the following set-up:

| Type | Description                                                                |
| ---- | -------------------------------------------------------------------------- |
|  duo | Contains two LND nodes named `tranche-ping` and `tranche-pong` unified by <br> one single `tranche-bitcoind` service. 
|  uno | Only has one LND node named `tranche-lnd` connected to `tranche-bitcoind`. |

### Peripheral containers

This project also helps you setup peripheral services to make development process easier, too.
For example, if you want to deploy a duo-cluster with attached postgres database, run the following:

```sh
$ tranche deploy --postgres
> ...
$ tranche mine
> ╭───── containers ─────╮┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
> │ tranche-postgres     │┃ Name          ┃ Nodekey      ┃ Channels  ┃ Peers  ┃ Height ┃ Synced? ┃
> │ tranche-pong         │┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
> │ tranche-ping         ││ tranche-pong  │ 3da33d3eb12  │ 2         │ 1      │ 216    │    true │
> │ tranche-bitcoind     ││               │ deacf4e1a64  │           │        │        │         │
> │ ...                  ││ ...           │ ...          │ ...       │ ...    │ ...    │ ...     │
```

Or run an uno-cluster with both attached postgres database and redis solid store cache like this:

```sh
$ tranche deploy --uno --postgres --redis
> ...
$ tranche mine
> ╭───── containers ─────╮┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
> │ tranche-postgres     │┃ Name          ┃ Nodekey      ┃ Channels  ┃ Peers  ┃ Height ┃ Synced? ┃
> │ tranche-redis        │┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
> │ tranche-lnd          ││ tranche-lnd   │ c0ae6b158d0  │ 0         │ 0      │ 202    │    true │
> │ tranche-bitcoind     ││               │ 4194459b8f3  │           │        │        │         │
> │ ...                  ││ ...           │ ...          │ ...       │ ...    │ ...    │ ...     │
```

## Cleanup

Use the following command to clean up active `tranche-*` containers:

```sh
tranche clean
```

🚧  This will resets the current test state, so use with care. Example below:

```sh
$ tranche clean
> Remove active containers:                  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:01
```

## Roadmap

* Add `tranche-lnd-krub` peripheral service using [lnd-krub](https://github.com/krutt/lnd-krub)
* Add `tranche-tesla-ball` peripheral service using [tesla-ball](https://github.com/krutt/tesla-ball)
* Write [click](https://click.palletsprojects.com) tests.
* Make image versioning a little bit more intuitive.
* Add `tranche-ord` peripheral service using [ord](https://github.com/ordinals/ord)
* Add `tranche-bitvm` peripheral service using [BitVM](https://github.com/BitVM/BitVM)
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
> Installing the current project: tranche (0.2.5)
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