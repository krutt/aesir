#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/ping_pong.py
# VERSION: 	   0.2.2
# CREATED: 	   2023-12-01 06:18
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from typing import Dict, List

### Third-party packages ###
from click import argument, command
from docker import DockerClient, from_env
from docker.models.containers import Container
from pydantic import TypeAdapter, ValidationError
from rich.progress import track

### Local modules ###
from src.schemas import LNDInfo, OpenChannel


@command
@argument("channel_size", default=16777215)
def ping_pong(channel_size: int) -> None:
    """For "duo" cluster, create channels between LND nodes."""
    client: DockerClient = from_env()
    if client.ping():
        nodekeys: Dict[str, str] = {}
        containers: List[Container] = client.containers.list()

        ### Fetch nodekeys ###
        for container in track(containers, "Fetch LND nodekeys:".ljust(42)):
            if match(r"tranche-ping|tranche-pong", container.name) is not None:
                lnd_info: LNDInfo = TypeAdapter(LNDInfo).validate_json(
                    container.exec_run(
                        """
                        lncli
                            --macaroonpath=/home/lnd/.lnd/data/chain/bitcoin/regtest/admin.macaroon
                            --rpcserver=localhost:10001
                            --tlscertpath=/home/lnd/.lnd/tls.cert
                        getinfo
                        """
                    ).output
                )
                nodekeys[container.name] = lnd_info.identity_pubkey

        ### Open channels ###
        errors: List[str] = []
        funding_txids: List[str] = []
        for container in track(containers, "Open channels:".ljust(42)):
            if container.name == "tranche-ping":
                try:
                    open_channel: OpenChannel = TypeAdapter(OpenChannel).validate_json(
                        container.exec_run(
                            """
                        lncli
                            --macaroonpath=/home/lnd/.lnd/data/chain/bitcoin/regtest/admin.macaroon
                            --rpcserver=localhost:10001
                            --tlscertpath=/home/lnd/.lnd/tls.cert
                        openchannel %d
                            --node_key %s
                            --connect tranche-pong:9735
                        """
                            % (channel_size, nodekeys.get("tranche-pong", ""))
                        ).output
                    )
                    funding_txids.append(open_channel.funding_txid)
                except ValidationError:
                    errors.append("!! Channel between tranche-ping to tranche-pong already opened.")
            elif container.name == "tranche-pong":
                try:
                    open_channel: OpenChannel = TypeAdapter(OpenChannel).validate_json(
                        container.exec_run(
                            """
                        lncli
                            --macaroonpath=/home/lnd/.lnd/data/chain/bitcoin/regtest/admin.macaroon
                            --rpcserver=localhost:10001
                            --tlscertpath=/home/lnd/.lnd/tls.cert
                        openchannel %d
                            --node_key %s
                            --connect tranche-ping:9735
                        """
                            % (channel_size, nodekeys.get("tranche-ping", ""))
                        ).output
                    )
                    funding_txids.append(open_channel.funding_txid)
                except ValidationError:
                    errors.append("!! Channel between tranche-pong to tranche-ping already opened.")
        print(f"Funding transactions: { funding_txids }")
        for error in errors:
            print(error)


__all__ = ["ping_pong"]
