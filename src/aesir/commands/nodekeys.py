#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/nodekeys.py
# VERSION: 	   0.4.1
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
from docker.errors import DockerException
from docker.models.containers import Container
from pydantic import TypeAdapter
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from aesir.types import LNDInfo


@command
def nodekeys() -> None:
  """Fetch nodekeys from active LND containers."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  lnds: List[Container] = list(
    filter(
      lambda container: match(r"aesir-lnd|aesir-ping|aesir-pong", container.name),
      reversed(client.containers.list()),
    )
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
    outputs.append(f"<Nodekey: '{ container.name }', '{ lnd_info.identity_pubkey }'>")
  list(map(rich_print, outputs))


__all__ = ["nodekeys"]
