#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/clean.py
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
from click import Context, command, pass_context
from docker import DockerClient, from_env
from docker.errors import NotFound
from docker.models.networks import Network
from rich.progress import track

### Local modules ###
from src.configs import NETWORK


@command
@pass_context
def clean(context: Context) -> None:
    """Remove all active "tranche-*" containers, drop network."""
    client: DockerClient = from_env()
    if client.ping():
        for container in track(client.containers.list(), "Remove active containers:".ljust(42)):
            if match(r"tranche-*", container.name) is not None:
                container.stop()
                container.remove()
        try:
            tranche_network: Network = client.networks.get(NETWORK)
            tranche_network.remove()
        except NotFound:
            pass


__all__ = ["clean"]
