#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/clean.py
# VERSION:     0.5.1
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from typing import List, Tuple

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import APIError, NotFound
from docker.models.containers import Container
from docker.models.networks import Network
from rich import print as rich_print
from rich.progress import track
from requests.exceptions import JSONDecodeError

### Local modules ###
from aesir.configs import NETWORK


@command
@option("--inactive", help="Query inactive containers for removal.", is_flag=True, type=bool)
def clean(inactive: bool) -> None:
  """Remove all active "aesir-*" containers, drop network."""
  try:
    client: DockerClient = from_env()
    client.ping()
  except APIError:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  outputs: List[str] = []
  containers: List[Container] = client.containers.list(all=inactive)
  for container in track(containers, f"Clean {('active','all')[inactive]} containers:".ljust(42)):
    if match(r"aesir-*", container.name) is not None:
      try:
        container.stop()
      except JSONDecodeError:
        pass
      container.remove(v=True)  # if `v` is true, remove associated volume
      outputs.append(f"<Container '{ container.name }'> removed.")
  try:
    network: Network = client.networks.get(NETWORK)
    network.remove()
    outputs.append(f"<Network '{ NETWORK }'> removed.")
  except NotFound:
    pass
  list(map(rich_print, outputs))


__all__: Tuple[str, ...] = ("clean",)
