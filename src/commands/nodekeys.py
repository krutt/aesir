#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/nodekeys.py
# VERSION: 	   0.2.6
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
from click import command
from docker import DockerClient, from_env
from docker.models.containers import Container
from pydantic import TypeAdapter
from rich.progress import track

### Local modules ###
from src.schemas import LNDInfo


@command
def nodekeys() -> None:
    """Fetch nodekeys from active LND containers."""
    client: DockerClient = from_env()
    if client.ping():
        containers: List[Container] = reversed(client.containers.list())  # type: ignore[assignment]
        lnds: List[Container] = list(
            filter(lambda c: match(r"aesir-lnd|aesir-ping|aesir-pong", c.name), containers)
        )
        outputs: List[str] = []
        for container in track(lnds, "Fetch LND nodekeys:".ljust(42)):
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
            outputs.append(f"<Nodekey: '{container.name}', '{lnd_info.identity_pubkey}'>")
        list(map(print, outputs))


__all__ = ["nodekeys"]
