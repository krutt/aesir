#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/faucet.py
# VERSION:     0.5.2
# CREATED:     2025-06-06 14:45
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from typing import List, Tuple

### Third-party packages ###
from click import argument, command
from docker import DockerClient, from_env
from docker.errors import APIError
from docker.models.containers import Container
from pydantic import validate_call
from rich import print as rich_print


@argument("sat_per_vbyte", default=21)
@argument("amount", default=1_000_000)
@argument("address")
@command
@validate_call
def faucet(address: str, amount: int, sat_per_vbyte: int) -> None:
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
      rich_print(
        container.exec_run(
          f"""
          lncli
            --macaroonpath=/root/.lnd/data/chain/bitcoin/regtest/admin.macaroon
            --rpcserver=localhost:10001
            --tlscertpath=/root/.lnd/tls.cert
          sendcoins --sat_per_vbyte=21 {address} {amount}
          """
        ).output.decode("utf-8")
      )

  list(map(rich_print, addresses))


__all__: Tuple[str, ...] = ("faucet",)
