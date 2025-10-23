#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/build.py
# VERSION:     0.5.4
# CREATED:     2024-02-27 23:52
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from io import BytesIO

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import DockerException, BuildError
from pydantic import ValidationError
from rich import print as rich_print
from rich.progress import TaskID

### Local modules ###
from aesir.configs import BUILDS
from aesir.exceptions import BuildUnsuccessful
from aesir.types import Build, BuildEnum
from aesir.views import Yggdrasil


@command
@option("--bitcoind", is_flag=True, help="Build bitcoind image", type=bool)
@option("--bitcoind-cat", is_flag=True, help="Build bitcoind-cat optional image", type=bool)
@option("--cashu-mint", is_flag=True, help="Build cashu-mint optional image", type=bool)
@option("--electrs", is_flag=True, help="Build electrs optional image", type=bool)
@option("--litd", is_flag=True, help="Build litd optional image", type=bool)
@option("--lnd", is_flag=True, help="Build lnd image", type=bool)
@option("--ord-server", is_flag=True, help="Build ord-server optional image", type=bool)
def build(
  bitcoind: bool,
  bitcoind_cat: bool,
  cashu_mint: bool,
  electrs: bool,
  litd: bool,
  lnd: bool,
  ord_server: bool,
) -> None:
  """Build peripheral images for the desired cluster."""
  try:
    client: DockerClient = from_env()
    client.ping()
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  ### Build optional images ###
  image_names: list[str] = list(
    map(
      lambda image: image.tags[0].split(":")[0],
      filter(lambda image: len(image.tags) != 0, client.images.list()),
    )
  )
  build_select: dict[BuildEnum, bool] = {
    "aesir-bitcoind": bitcoind,
    "aesir-bitcoind-cat": bitcoind_cat,
    "aesir-cashu-mint": cashu_mint,
    "aesir-electrs": electrs,
    "aesir-litd": litd,
    "aesir-lnd": lnd,
    "aesir-ord-server": ord_server,
  }

  outputs: list[str] = []
  built: set[str] = {tag for tag in BUILDS.keys() if build_select[tag] and tag in image_names}
  outputs += map(lambda tag: f"<Image: '{tag}'> already exists within images.", built)
  list(map(rich_print, outputs))

  builds: dict[str, Build] = {
    tag: build for tag, build in BUILDS.items() if build_select[tag] and tag not in image_names
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
                decode=True, fileobj=fileobj, gzip=True, platform=build.platform, rm=True, tag=tag
              ),
              build_task_id,
            )
          except (BuildError, BuildUnsuccessful, ValidationError):
            yggdrasil.update(build_task_id, completed=-1)
            continue
          yggdrasil.update(build_task_id, completed=100)
          yggdrasil.update(task_id, advance=1)
      yggdrasil.update(task_id, completed=build_count, description="[blue]Complete[reset]")


__all__: tuple[str, ...] = ("build",)
