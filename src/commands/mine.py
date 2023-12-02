#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/nodekeys.py
# VERSION: 	   0.2.1
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from typing import List

### Third-party packages ###
from apscheduler.schedulers.background import BackgroundScheduler
from click import argument, command
from docker import DockerClient, from_env
from docker.errors import NotFound
from docker.models.containers import Container
from pydantic import TypeAdapter
from rich.json import JSON
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import track

### Local modules ###
from src.schemas import BlockchainInfo, NewAddress, NodeInfo


@command
@argument("blockcount", default=1, type=int)
@argument("blocktime", default=5, type=int)
def mine(blockcount: int, blocktime: int) -> None:
    """Scheduled mining with "blockcount" and "blocktime"."""
    client: DockerClient = from_env()
    if client.ping():
        mining_targets: List[str] = []
        for container in track(client.containers.list(), "Generate mining treasuries:".ljust(35)):
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
        bitcoind: Container
        try:
            bitcoind = client.containers.get("tranche-bitcoind")
        except NotFound:
            print('!! Unable to find "tranche-bitcoind" container.')
            return
        scheduler: BackgroundScheduler = BackgroundScheduler()
        for address in mining_targets:
            scheduler.add_job(
                bitcoind.exec_run,
                "interval",
                [
                    """
                    bitcoin-cli
                        -regtest
                        -rpcuser=tranche
                        -rpcpassword=tranche
                    generatetoaddress %d %s
                    """
                    % (blockcount, address)
                ],
                seconds=blocktime,
            )
        scheduler.start()
        pane: Layout = Layout()
        pane.split_row(
            Layout(name="bitcoind", size=30),
            Layout(name="lightning", size=70),
        )
        with Live(pane, refresh_per_second=4, transient=True) as live:
            while True:
                info: BlockchainInfo = TypeAdapter(BlockchainInfo).validate_json(
                    bitcoind.exec_run(
                        """
                        bitcoin-cli -regtest -rpcuser=tranche -rpcpassword=tranche getblockchaininfo
                        """
                    ).output
                )
                pane["bitcoind"].update(Panel(JSON.from_data(info.model_dump()), title="bitcoind"))

                node_infos: List[NodeInfo] = []
                for container in client.containers.list():
                    if match("tranche-lnd|tranche-ping|tranche-pong", container.name) is not None:
                        node_info: NodeInfo = TypeAdapter(NodeInfo).validate_json(
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
                        node_infos.append(node_info)
                # if


__all__ = ["mine"]
