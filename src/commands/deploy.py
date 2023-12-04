#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/deploy.py
# VERSION: 	   0.2.8
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from time import sleep
from typing import Dict, List

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import APIError, DockerException, NotFound
from docker.models.containers import Container
from pydantic import TypeAdapter
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from src.configs import CLUSTERS, IMAGES, NETWORK, PERIPHERALS
from src.schemas import MutexOption, NewAddress, Service, ServiceName


@command
@option("--duo", alternatives=["uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--uno", alternatives=["duo"], cls=MutexOption, is_flag=True, type=bool)
@option("--with-postgres", is_flag=True, help="Deploy postgres peripheral service", type=bool)
@option("--with-redis", is_flag=True, help="Deploy redis peripheral service", type=bool)
def deploy(duo: bool, uno: bool, with_postgres: bool, with_redis: bool) -> None:
    """Deploy cluster, either with one or two LND nodes."""
    client: DockerClient
    try:
        client = from_env()
        if not client.ping():
            raise DockerException
    except DockerException:
        rich_print("[red bold]Unable to connect to docker daemon.")
        return

    ### Defaults to duo network; Derive cluster information from parameters ###
    duo = duo or (not duo and not uno)  # defaults to duo network
    cluster: Dict[ServiceName, Service] = (CLUSTERS["duo"], CLUSTERS["uno"])[uno]
    peripheral_select: Dict[str, bool] = {"postgres": with_postgres, "redis": with_redis}
    peripherals: Dict[ServiceName, Service] = {
        f"aesir-{k}": v[f"aesir-{k}"] for k, v in PERIPHERALS.items() if peripheral_select[k]  # type: ignore[index, misc]
    }
    cluster.update(peripherals)

    ### Attempts to create network if not exist ###
    try:
        client.networks.create(NETWORK, check_duplicate=True)
    except APIError:
        pass

    ### Deploy specified cluster ###
    for name, service in track(cluster.items(), f"Deploy {('duo', 'uno')[uno]} cluster:".ljust(42)):
        image_name: str = dict(**IMAGES["required"], **IMAGES["optional"])[service.alias]
        ports: Dict[str, str] = dict(
            map(lambda item: (item[0], item[1]), [port.split(":") for port in service.ports])
        )
        client.containers.run(
            image_name,
            command=service.command,
            detach=True,
            environment=service.env_vars,
            name=name,
            network=NETWORK,
            ports=ports,
        )

    ### Wait until lnd(s) ready ###
    sleep(3)

    ### Mine starting capital ###
    treasuries: List[str] = []
    for container in track(client.containers.list(), "Generate addresses:".ljust(42)):
        if match(r"aesir-lnd|aesir-ping|aesir-pong", container.name) is not None:
            new_address: NewAddress = TypeAdapter(NewAddress).validate_json(
                container.exec_run(
                    """
                    lncli
                        --macaroonpath=/home/lnd/.lnd/data/chain/bitcoin/regtest/admin.macaroon
                        --rpcserver=localhost:10001
                        --tlscertpath=/home/lnd/.lnd/tls.cert
                    newaddress p2wkh
                    """
                ).output
            )
            treasuries.append(new_address.address)

    ### Retrieve bitcoind container ###
    bitcoind: Container
    try:
        bitcoind = client.containers.get("aesir-bitcoind")
    except NotFound:
        rich_print('!! Unable to find "aesir-bitcoind" container.')
        return
    for address in track(treasuries, "Mine initial capital for parties:".ljust(42)):
        bitcoind.exec_run(
            """
            bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir generatetoaddress 101 %s
            """
            % address
        )


__all__ = ["deploy"]
