#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/mine.py
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
from apscheduler.schedulers.background import BackgroundScheduler
from click import argument, command
from docker import DockerClient, from_env
from docker.errors import APIError, NotFound
from docker.models.containers import Container
from pydantic import TypeAdapter
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from aesir.views import Bifrost
from aesir.types import NewAddress


@command
@argument("blockcount", default=1, type=int)
@argument("blocktime", default=5, type=int)
def mine(blockcount: int, blocktime: int) -> None:
  """Scheduled mining with "blockcount" and "blocktime"."""
  try:
    client: DockerClient = from_env()
    client.ping()
  except APIError:
    rich_print("[red bold]Unable to connect to daemon.")
    return

  ### Retrieve bitcoind container ###
  bitcoind: Container
  try:
    bitcoind = client.containers.get("aesir-bitcoind")
  except NotFound:
    try:
      bitcoind = client.containers.get("aesir-bitcoind-cat")
    except NotFound:
      rich_print('[red bold]Unable to find "aesir-bitcoind" container.')
      return

  ### Retrieve other containers ###
  aesir_containers: List[Container] = list(
    filter(lambda container: match(r"aesir-*", container.name), reversed(client.containers.list()))
  )
  container_names: List[str] = list(map(lambda container: container.name, aesir_containers))
  lnd_containers: List[Container] = list(
    filter(lambda container: match(r"aesir-(lnd|ping|pong)", container.name), aesir_containers)
  )

  ### Generate treasury addresses as mining destinations ###
  treasuries: List[str] = []
  if len(lnd_containers) == 0:
    bitcoind.exec_run(
      """
      bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir createwallet default
      """
    )
    treasury_address: str = bitcoind.exec_run(
      """
      bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir getnewaddress treasury bech32
      """
    ).output.decode("utf-8")
    treasuries.append(treasury_address)
  else:
    for container in track(lnd_containers, "Generate mining treasuries:".ljust(42)):
      new_address: NewAddress = TypeAdapter(NewAddress).validate_json(
        container.exec_run(
          """
          lncli
            --macaroonpath=/home/lnd/.lnd/data/chain/bitcoin/regtest/admin.macaroon
            --rpcserver=localhost:10001
            --tlscertpath=/home/lnd/.lnd/tls.cert
          newaddress p2wkh
          """
        )
      )
      treasuries.append(new_address.address)

  ### Set up mining schedule using command arguments ###
  scheduler: BackgroundScheduler = BackgroundScheduler()
  for address in treasuries:
    scheduler.add_job(
      bitcoind.exec_run,
      "interval",
      [
        """
        bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir generatetoaddress %d %s
        """
        % (blockcount, address)
      ],
      seconds=blocktime,
    )
  scheduler.start()

  bifrost: Bifrost = Bifrost(
    bitcoind=bitcoind,
    containers=aesir_containers,
    container_index=0,
    container_names=container_names,
  )
  bifrost.display()


__all__: Tuple[str, ...] = ("mine",)
