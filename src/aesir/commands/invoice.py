#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/invoice.py
# VERSION:     0.5.1
# CREATED:     2024-11-15 00:56
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, Tuple
from uuid import uuid4 as uuid

### Third-party packages ###
from click import argument, command, option
from docker import DockerClient, from_env
from docker.errors import APIError, NotFound
from docker.models.containers import Container
from pydantic import TypeAdapter
from rich import print as rich_print

### Local modules ###
from aesir.types import LNDInvoice, MutexOption, ServiceName


@argument("amount", default=1_000)
@argument("memo", default=str(uuid()))
@command
@option("--lnd", alternatives=["ping", "pong"], cls=MutexOption, is_flag=True, type=bool)
@option("--ping", alternatives=["lnd", "pong"], cls=MutexOption, is_flag=True, type=bool)
@option("--pong", alternatives=["lnd", "ping"], cls=MutexOption, is_flag=True, type=bool)
def invoice(amount: int, lnd: bool, memo: str, ping: bool, pong: bool) -> None:
  """For either "uno" or "duo" cluster, create an invoice from specified lnd container"""
  try:
    client: DockerClient = from_env()
    client.ping()
  except APIError:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  ### Select LND container from specified mutually exclusive options ###
  container_name: ServiceName = "aesir-lnd"
  container_selector: Dict[ServiceName, bool] = {
    "aesir-lnd": lnd,
    "aesir-ping": ping,
    "aesir-pong": pong,
  }
  try:
    container_name = next(filter(lambda key_values: key_values[1], container_selector.items()))[0]
  except StopIteration:
    pass

  ### Initiate parameters ###
  container: Container
  try:
    container = client.containers.get(container_name)
  except NotFound:
    rich_print(f'[red bold]Unable to find specified LND container (name="{ container_name }")')
    return

  ### Generate invoice ###
  lnd_invoice: LNDInvoice = TypeAdapter(LNDInvoice).validate_json(
    container.exec_run(
      f"""
      lncli
        --macaroonpath=/home/lnd/.lnd/data/chain/bitcoin/regtest/admin.macaroon
        --rpcserver=localhost:10001
        --tlscertpath=/home/lnd/.lnd/tls.cert
      addinvoice
        --amt={ amount }
        --memo={ memo }
      """
    ).output
  )
  rich_print(lnd_invoice)


__all__: Tuple[str, ...] = ("invoice",)
