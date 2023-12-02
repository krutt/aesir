#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/deploy.py
# VERSION: 	   0.2.3
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
from docker.errors import APIError
from docker.models.containers import Container
from pydantic import TypeAdapter
from rich.progress import track

### Local modules ###
from src.configs import CLUSTERS, IMAGES, NETWORK
from src.schemas import MutexOption, NewAddress, Service, ServiceName


@command
@option("--duo", alternatives=["uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--uno", alternatives=["duo"], cls=MutexOption, is_flag=True, type=bool)
def deploy(duo: bool, uno: bool) -> None:
    """Deploy cluster, either with one or two LND nodes."""
    duo = duo or (not duo and not uno)  # defaults to duo network
    cluster: Dict[ServiceName, Service] = (CLUSTERS["duo"], CLUSTERS["uno"])[uno]
    client: DockerClient = from_env()
    if client.ping():
        try:
            client.networks.create(NETWORK, check_duplicate=True)
        except APIError:
            pass
        for name, service in track(cluster.items(), "Deploy specified local cluster:".ljust(42)):
            image_name: str = IMAGES[service.alias]
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
        sleep(3)  # wait until lnd ready
        mining_targets: List[str] = []
        for container in track(client.containers.list(), "Generate addresses:".ljust(42)):
            if match(r"tranche-lnd|tranche-ping|tranche-pong", container.name) is not None:
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
                mining_targets.append(new_address.address)
        bitcoind: Container = client.containers.get("tranche-bitcoind")
        for address in track(mining_targets, "Mine initial capital for parties:".ljust(42)):
            bitcoind.exec_run(
                """
                bitcoin-cli -regtest -rpcuser=tranche -rpcpassword=tranche generatetoaddress 101 %s
                """
                % address
            )


__all__ = ["deploy"]
