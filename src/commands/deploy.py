#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/deploy.py
# VERSION: 	   0.3.0
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from time import sleep
from typing import Dict, Literal

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
@option("--with-lnd-krub", is_flag=True, help="Deploy lnd-krub peripheral service", type=bool)
@option("--with-postgres", is_flag=True, help="Deploy postgres peripheral service", type=bool)
@option("--with-redis", is_flag=True, help="Deploy redis peripheral service", type=bool)
def deploy(
    duo: bool, uno: bool, with_lnd_krub: bool, with_postgres: bool, with_redis: bool
) -> None:
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
    peripheral_select: Dict[str, bool] = {
        "lnd-krub": False,
        "postgres": with_postgres,
        "redis": with_redis,
    }
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
    lnds: Dict[ServiceName, Literal["address", "certificate", "macaroon"]] = {}
    for container in track(client.containers.list(), "Generate addresses:".ljust(42)):
        if match(r"aesir-lnd|aesir-ping|aesir-pong", container.name) is not None:
            certificate: str = (
                container.exec_run(
                    """
                cat /home/lnd/.lnd/tls.cert
                """
                )
                .output.decode("utf-8")
                .replace("\n", "\\n")
            )
            # macaroon: str = container.exec_run(
            #     """
            #     cat /home/lnd/.lnd/data/chain/bitcoin/regtest/invoices.macaroon
            #     """
            # ).output.decode("iso-8859-1").replace("\n", "\\n")
            # macaroon: str = container.exec_run(
            #     """
            #     lncli
            #         --macaroonpath=/home/lnd/.lnd/data/chain/bitcoin/regtest/admin.macaroon
            #         --rpcserver=localhost:10001
            #         --tlscertpath=/home/lnd/.lnd/tls.cert
            #     bakemacaroon invoices:read invoices:write
            #     """
            # ).output.decode("utf-8").replace("\n", "\\n")
            macaroon: str = ""
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
            lnds[container.name] = {
                "address": new_address.address,
                "certificate": certificate,
                "macaroon": macaroon,
            }

    # print(lnds)
    # return
    if with_lnd_krub:
        service: Service = PERIPHERALS["lnd-krub"]["aesir-lnd-krub"]
        macaroon: str = lnds["aesir-ping"]["macaroon"]  # .decode("utf-8")
        tlscert: str = lnds["aesir-ping"]["certificate"]  # .decode("utf-8")
        ports: Dict[str, str] = dict(  # type: ignore[no-redef]
            map(lambda item: (item[0], item[1]), [port.split(":") for port in service.ports])
        )
        client.containers.run(
            "lnd-krub",
            command=[],
            detach=True,
            environment=service.env_vars + [f"MACAROON={macaroon}", f"TLSCERT={tlscert}"],
            name="aesir-lnd-krub",
            network=NETWORK,
            ports=ports,
        )

    ### Retrieve bitcoind container ###
    bitcoind: Container
    try:
        bitcoind = client.containers.get("aesir-bitcoind")
    except NotFound:
        rich_print('[dim yellow1]Unable to find "aesir-bitcoind"; initial capital not yet mined.')
        return
    for address, _, _ in track(lnds.values(), "Mine initial capital for parties:".ljust(42)):
        bitcoind.exec_run(
            """
            bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir generatetoaddress 101 %s
            """
            % address
        )


__all__ = ["deploy"]
