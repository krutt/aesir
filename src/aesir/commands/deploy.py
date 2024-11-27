#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/deploy.py
# VERSION:     0.4.9
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
from typing import Dict, List

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import APIError, BuildError, DockerException, ImageNotFound, NotFound
from docker.models.containers import Container
from pydantic import TypeAdapter
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from aesir.configs import BUILDS, CLUSTERS, IMAGES, NETWORK, PERIPHERALS
from aesir.types import Build, MutexOption, NewAddress, Service, ServiceName
from aesir.views import Yggdrasil


@command
@option("--cat", alternatives=["duo", "ohm", "uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--duo", alternatives=["cat", "ohm", "uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--ohm", alternatives=["cat", "duo", "uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--uno", alternatives=["cat", "duo", "ohm"], cls=MutexOption, is_flag=True, type=bool)
@option("--with-cashu-mint", is_flag=True, help="Deploy cashu-mint peripheral service", type=bool)
@option("--with-lnd-krub", is_flag=True, help="Deploy lnd-krub peripheral service", type=bool)
@option("--with-ord-server", is_flag=True, help="Deploy ord-server peripheral service", type=bool)
@option("--with-postgres", is_flag=True, help="Deploy postgres peripheral service", type=bool)
@option("--with-redis", is_flag=True, help="Deploy redis peripheral service", type=bool)
def deploy(
  cat: bool,
  duo: bool,
  ohm: bool,
  uno: bool,
  with_cashu_mint: bool,
  with_lnd_krub: bool,
  with_ord_server: bool,
  with_postgres: bool,
  with_redis: bool,
) -> None:
  """Deploy cluster, either with one or two LND nodes."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  ### Defaults to duo network; Derive cluster information from parameters ###
  selector: Dict[ServiceName, bool] = {"cat": cat, "duo": duo, "ohm": ohm, "uno": uno}
  cluster_name: ServiceName = "duo"
  try:
    cluster_name = next(filter(lambda value: value[1], selector.items()))[0]
  except StopIteration:
    pass
  cluster: Dict[ServiceName, Service] = CLUSTERS[cluster_name]
  selector = {
    "cashu-mint": False,
    "lnd-krub": False,
    "ord-server": False,
    "postgres": with_postgres,
    "redis": with_redis,
  }
  peripherals: Dict[ServiceName, Service] = {
    f"aesir-{key}": value[f"aesir-{key}"]  # type: ignore[index, misc]
    for key, value in PERIPHERALS.items()
    if selector[key]
  }
  cluster.update(peripherals)

  ### Attempts to create network if not exist ###
  try:
    client.networks.create(NETWORK, check_duplicate=True)
  except APIError:
    pass

  ### Deploy specified cluster ###
  for name, service in track(cluster.items(), f"Deploy { cluster_name } cluster:".ljust(42)):
    image_name: str = dict(**IMAGES["required"], **IMAGES["optional"])[service.alias]
    ports: Dict[str, str] = dict(
      map(lambda item: (item[0], item[1]), [port.split(":") for port in service.ports])
    )
    client.containers.run(
      image_name,
      command=service.command,
      detach=True,
      environment=service.env_vars,
      name=name,
      network=NETWORK,
      ports=ports,
    )

  treasuries: List[str] = []
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
              --macaroonpath=/home/lnd/.lnd/data/chain/bitcoin/regtest/admin.macaroon
              --rpcserver=localhost:10001
              --tlscertpath=/home/lnd/.lnd/tls.cert
            newaddress p2wkh
            """
          ).output
        )
        treasuries.append(new_address.address)

  ### Define selection for shared-volume peripherals ###
  selector = {
    "bitcoind-cat": False,
    "cashu-mint": with_cashu_mint,
    "lnd-krub": with_lnd_krub and with_postgres and with_redis,
    "ord-server": with_ord_server,
    "postgres": False,
    "redis": False,
  }

  ### Build missing images if any for shared-volume peripherals ###
  image_names: List[str] = list(
    map(
      lambda image: image.tags[0].split(":")[0],
      filter(lambda image: len(image.tags) != 0, client.images.list()),
    )
  )
  builds: Dict[str, Build] = {
    tag: build for tag, build in BUILDS.items() if selector[tag] and tag not in image_names
  }
  build_count: int = len(builds.keys())
  if build_count != 0:
    builds_items = builds.items()
    with Yggdrasil(row_count=10) as yggdrasil:
      task_id: int = yggdrasil.add_task("", progress_type="primary", total=build_count)
      for tag, build in builds_items:
        build_task_id: int = yggdrasil.add_task(tag, progress_type="build", total=100)
        with BytesIO("\n".join(build.instructions).encode("utf-8")) as fileobj:
          try:
            yggdrasil.progress_build(  # type: ignore[misc]
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

  ### Deploy shared volume peripherals ###
  run_errors: List[str] = []
  peripherals = {f"aesir-{k}": v[f"aesir-{k}"] for k, v in PERIPHERALS.items() if selector[k]}  # type: ignore[index, misc]
  volume_target: str = "aesir-ping" if duo else "aesir-lnd"
  for name, service in track(peripherals.items(), "Deploy shared-volume peripherals:".ljust(42)):
    ports = dict(map(lambda item: (item[0], item[1]), [port.split(":") for port in service.ports]))
    volume_target = "aesir-bitcoind" if name == "aesir-ord" else volume_target
    try:
      client.containers.run(
        service.alias,
        command=service.command,
        detach=True,
        environment=service.env_vars,
        name=name,
        network=NETWORK,
        ports=ports,
        volumes_from=[volume_target],
      )
    except ImageNotFound:
      run_errors.append(
        f"<[bright_magenta]Image [green]'{ service.alias }'[reset]> [red]is not found.[reset]"
      )
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

  ### Show warnings ###
  warnings: List[str] = []
  if with_lnd_krub and (not with_postgres or not with_redis):
    warnings.append("[dim yellow1]LNDKrub needs to be launched in tandem with Postgres and Redis.")
  list(map(rich_print, warnings))


__all__ = ("deploy",)
