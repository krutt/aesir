#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/deploy.py
# VERSION:     0.5.4
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from io import BytesIO
from re import match
from time import sleep
from typing import Iterator

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import APIError, BuildError, DockerException, ImageNotFound, NotFound
from docker.models.containers import Container
from pydantic import TypeAdapter
from rich import print as rich_print
from rich.progress import TaskID, track

### Local modules ###
from aesir.configs import BUILDS, CLUSTERS, NETWORK, PERIPHERALS
from aesir.types import (
  Build,
  BuildEnum,
  ClusterEnum,
  MutexOption,
  NewAddress,
  Service,
  ServiceName,
)
from aesir.views import Yggdrasil


@command
@option("--cat", alternatives=["duo", "ohm", "uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--duo", alternatives=["cat", "ohm", "uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--ohm", alternatives=["cat", "duo", "uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--uno", alternatives=["cat", "duo", "ohm"], cls=MutexOption, is_flag=True, type=bool)
@option("--with-cashu-mint", is_flag=True, help="Deploy cashu-mint peripheral service", type=bool)
@option("--with-electrs", is_flag=True, help="Deploy electrs peripheral service", type=bool)
@option("--with-litd", is_flag=True, help="Deploy litd peripheral service", type=bool)
@option("--with-ord-server", is_flag=True, help="Deploy ord-server peripheral service", type=bool)
@option("--with-postgres", is_flag=True, help="Deploy postgres peripheral service", type=bool)
@option("--with-redis", is_flag=True, help="Deploy redis peripheral service", type=bool)
def deploy(
  cat: bool,
  duo: bool,
  ohm: bool,
  uno: bool,
  with_cashu_mint: bool,
  with_electrs: bool,
  with_litd: bool,
  with_ord_server: bool,
  with_postgres: bool,
  with_redis: bool,
) -> None:
  """Deploy cluster, either with one or two LND nodes."""
  try:
    client: DockerClient = from_env()
    client.ping()
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  ### Defaults to duo network; Derive cluster information from parameters ###
  cluster_selector: dict[ClusterEnum, bool] = {"cat": cat, "duo": duo, "ohm": ohm, "uno": uno}
  cluster_name: ClusterEnum = "duo"
  try:
    cluster_name = next(filter(lambda value: value[1], cluster_selector.items()))[0]
  except StopIteration:
    pass
  cluster: dict[ServiceName, Service] = CLUSTERS[cluster_name]
  image_selector: dict[ServiceName, bool] = {
    "aesir-cashu-mint": False,
    "aesir-electrs": False,
    "aesir-litd": False,
    "aesir-ord-server": False,
    "aesir-postgres": with_postgres,
    "aesir-redis": with_redis,
  }
  peripherals: Iterator[tuple[ServiceName, Service]] = filter(
    lambda peripheral_tuple: image_selector[peripheral_tuple[0]], PERIPHERALS.items()
  )
  cluster.update(peripherals)

  ### Attempts to create network if not exist ###
  try:
    client.networks.create(NETWORK, check_duplicate=True)
  except APIError:
    pass

  ### Deploy specified cluster ###
  run_errors: list[str] = []
  for name, service in track(cluster.items(), f"Deploy {cluster_name} cluster:".ljust(42)):
    image_name: str = service.image
    flags: list[str] = list(service.command.values())
    ports: dict[str, str] = dict(
      map(lambda item: (item[0], item[1]), [port.split(":") for port in service.ports])
    )
    try:
      client.containers.run(
        image_name,
        command=flags,
        detach=True,
        environment=service.env_vars,
        name=name,
        network=NETWORK,
        ports=ports,
      )
    except APIError as err:
      run_errors.append(f"[red]Failed cluster setup due to: [reset]{err.explanation}")
      break
  if len(run_errors) != 0:
    list(map(rich_print, run_errors))
    return

  treasuries: list[str] = []
  if duo or uno:
    ### Wait until lnd(s) ready ###
    sleep(3)

    ### Mine starting capital ###
    for container in track(client.containers.list(), "Generate addresses:".ljust(42)):
      if match(r"aesir-lnd|aesir-ping|aesir-pong", container.name) is not None:
        new_address: NewAddress = TypeAdapter(NewAddress).validate_json(
          container.exec_run(
            """
            lncli
              --macaroonpath=/root/.lnd/data/chain/bitcoin/regtest/admin.macaroon
              --rpcserver=localhost:10009
              --tlscertpath=/root/.lnd/tls.cert
            newaddress p2wkh
            """
          ).output
        )
        treasuries.append(new_address.address)

  ### Define build targets for missing peripherals ###
  build_selector: dict[BuildEnum, bool] = {
    "aesir-bitcoind": False,
    "aesir-bitcoind-cat": False,
    "aesir-cashu-mint": with_cashu_mint,
    "aesir-electrs": with_electrs,
    "aesir-litd": with_litd,
    "aesir-lnd": False,
    "aesir-ord-server": with_ord_server,
  }

  ### Build missing images if any for shared-volume peripherals ###
  image_names: list[str] = list(
    map(
      lambda image: image.tags[0].split(":")[0],
      filter(lambda image: len(image.tags) != 0, client.images.list()),
    )
  )
  builds: dict[str, Build] = {
    tag: build for tag, build in BUILDS.items() if build_selector[tag] and tag not in image_names
  }
  build_count: int = len(builds.keys())
  if build_count != 0:
    builds_items = builds.items()
    with Yggdrasil(row_count=10) as yggdrasil:
      task_id: TaskID = yggdrasil.add_task("", progress_type="primary", total=build_count)
      for tag, build in builds_items:
        build_task_id: TaskID = yggdrasil.add_task(tag, progress_type="build", total=100)
        with BytesIO("\n".join(build.instructions).encode("utf-8")) as fileobj:
          try:
            yggdrasil.progress_build(
              client.api.build(
                decode=True, fileobj=fileobj, platform=build.platform, rm=True, tag=tag
              ),
              build_task_id,
            )
          except BuildError:
            yggdrasil.update(
              build_task_id,
              completed=0,
              description=f"[red bold]Build unsuccessful for <Image '{tag}'>.",
            )
          yggdrasil.update(
            build_task_id,
            completed=100,
            description=f"[blue]Built <[bright_magenta]Image [green]'{tag}'[reset]> successfully.",
          )
          yggdrasil.update(task_id, advance=1)
      yggdrasil.update(task_id, completed=build_count, description="[blue]Complete")

  ### Define selection for shared-volume peripherals ###
  shared_volume_selector: dict[str, bool] = {
    "aesir-cashu-mint": with_cashu_mint and (duo or uno),
    "aesir-electrs": with_electrs,
    "aesir-litd": with_litd,
    "aesir-ord-server": with_ord_server,
    "aesir-postgres": False,
    "aesir-redis": False,
  }
  peripherals = filter(
    lambda peripheral_tuple: shared_volume_selector[peripheral_tuple[0]], PERIPHERALS.items()
  )
  run_errors = []
  for name, service in track(peripherals, "Deploy shared-volume peripherals:".ljust(42)):
    volume_target: str = "aesir-bitcoind" if not cat else "aesir-bitcoind-cat"
    volume_target = (
      "aesir-lnd" if (name in {"aesir-cashu-mint", "aesir-litd"}) and uno else "aesir-ping"
    )
    flags = list(service.command.values())
    ports = dict(map(lambda item: (item[0], item[1]), [port.split(":") for port in service.ports]))
    try:
      client.containers.run(
        service.image,
        command=flags,
        detach=True,
        environment=service.env_vars,
        name=name,
        network=NETWORK,
        ports=ports,
        volumes_from=[volume_target],
      )
    except ImageNotFound:
      run_errors.append(
        f"<[bright_magenta]Image [green]'{service.image}'[reset]> [red]is not found.[reset]"
      )
  if with_cashu_mint and not (duo or uno):
    run_errors.append("[red]Cashu Mint needs to be run with at least one LND Node.[reset]")
  list(map(rich_print, run_errors))

  if len(treasuries) != 0:
    ### Retrieve bitcoind container ###
    bitcoind: Container
    try:
      bitcoind = client.containers.get("aesir-bitcoind")
    except NotFound:
      rich_print('[dim yellow1]Unable to find "aesir-bitcoind"; initial capital not yet mined.')
      return
    for address in track(treasuries, "Mine initial capital for parties:".ljust(42)):
      bitcoind.exec_run(
        """
        bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir generatetoaddress 101 %s
        """
        % address
      )


__all__: tuple[str, ...] = ("deploy",)
