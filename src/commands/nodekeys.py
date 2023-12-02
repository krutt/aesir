#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/nodekeys.py
# VERSION: 	   0.2.3
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match

### Third-party packages ###
from click import command
from docker import DockerClient, from_env
from pydantic import TypeAdapter
from rich.progress import track

### Local modules ###
from src.schemas import LNDInfo


@command
def nodekeys() -> None:
    """Fetch nodekeys from active LND containers."""
    client: DockerClient = from_env()
    if client.ping():
        for container in track(client.containers.list(), "Fetch LND nodekeys:".ljust(42)):
            if match(r"tranche-lnd|tranche-ping|tranche-pong", container.name) is not None:
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
                print(f"<Nodekey: '{container.name}', '{lnd_info.identity_pubkey}'>")


__all__ = ["nodekeys"]
