#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/ping_pong.py
# VERSION: 	   0.2.4
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
from docker.errors import NotFound
from docker.models.containers import Container
from pydantic import TypeAdapter, ValidationError
from rich.progress import track

### Local modules ###
from src.schemas import LNDInfo, NewAddress, OpenChannel


@command
@argument("channel_size", default=16777215)
def ping_pong(channel_size: int) -> None:
    """For "duo" cluster, create channels between LND nodes."""
    client: DockerClient = from_env()
    if client.ping():
        bitcoind: Container
        try:
            bitcoind = client.containers.get("tranche-bitcoind")
        except NotFound:
            print('!! Unable to find "tranche-bitcoind" container.')
            return
        containers: List[Container] = list(reversed(client.containers.list()))
        paddles: List[Container] = list(
            filter(lambda c: match(r"tranche-ping|tranche-pong", c.name), containers)
        )
        mining_targets: Dict[str, str] = {}
        nodekeys: Dict[str, str] = {}

        ### Fetch nodekeys ###
        for container in track(paddles, "Fetch LND nodekeys:".ljust(42)):
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
            mining_targets[container.name] = new_address.address

        ### Open channels ###
        outputs: List[str] = []
        for container in track(paddles, "Open channels:".ljust(42)):
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
                    outputs.append(
                        f"<Channel 'tranche-ping --> tranche-pong' : { open_channel.funding_txid }>"
                    )
                    bitcoind.exec_run(
                        """
                        bitcoin-cli -regtest -rpcuser=tranche -rpcpassword=tranche generatetoaddress %d %s
                        """
                        % (6, mining_targets.get("tranche-ping", ""))
                    )
                except ValidationError:
                    outputs.append("!! Channel 'tranche-ping --> tranche-pong' already opened.")
            elif container.name == "tranche-pong":
                try:
                    open_channel: OpenChannel = TypeAdapter(OpenChannel).validate_json(  # type: ignore[no-redef]
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
                    outputs.append(
                        f"<Channel 'tranche-pong --> tranche-ping' : { open_channel.funding_txid }>"
                    )
                    bitcoind.exec_run(
                        """
                        bitcoin-cli -regtest -rpcuser=tranche -rpcpassword=tranche generatetoaddress %d %s
                        """
                        % (6, mining_targets.get("tranche-pong", ""))
                    )
                except ValidationError:
                    outputs.append("!! Channel 'tranche-pong --> tranche-ping' already opened.")
        list(map(print, outputs))


__all__ = ["ping_pong"]
