#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/address.py
# VERSION:     0.5.2
# CREATED:     2025-06-06 14:45
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from typing import List, Literal, Tuple

### Third-party packages ###
from click import argument, command
from docker import DockerClient, from_env
from docker.errors import APIError
from docker.models.containers import Container
from pydantic import TypeAdapter, validate_call
from rich import print as rich_print

### Local modules ###
from aesir.types import NewAddress


@argument("address_type", default="p2wkh")
@command
@validate_call
def getnewaddress(address_type: Literal["p2wkh", "np2wkh", "p2tr"]) -> None:
  """ """
  try:
    client: DockerClient = from_env()
    client.ping()
  except APIError:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  aesir_containers: List[Container] = list(
    filter(lambda container: match(r"aesir-*", container.name), reversed(client.containers.list()))
  )
  addresses: List[str] = []
  lnd_containers: List[Container] = list(
    filter(
      lambda container: match(r"aesir-(lnd|ping)", container.name), aesir_containers
    )  # NOTE: skip pong
  )
  if len(lnd_containers) == 0:
    rich_print("[error]No LND nodes deployed currently.[reset]")
    return
  else:
    for container in lnd_containers:
      new_address: NewAddress = TypeAdapter(NewAddress).validate_json(
        container.exec_run(
          f"""
          lncli
            --macaroonpath=/root/.lnd/data/chain/bitcoin/regtest/admin.macaroon
            --rpcserver=localhost:10001
            --tlscertpath=/root/.lnd/tls.cert
          newaddress {address_type}
          """
        ).output
      )
      addresses.append(new_address.address)

  list(map(rich_print, addresses))


__all__: Tuple[str, ...] = ("getnewaddress",)
