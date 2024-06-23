#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/build.py
# VERSION:     0.4.3
# CREATED:     2024-02-27 23:52
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from io import BytesIO
from typing import Dict, List, Set

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import BuildError, DockerException
from rich import print as rich_print
from rich.progress import Progress

### Local modules ###
from aesir.configs import BUILDS
from aesir.types import Build


@command
@option("--bitcoind-cat", is_flag=True, help="Build bitcoind-cat optional image", type=bool)
@option("--cashu-mint", is_flag=True, help="Build cashu-mint optional image", type=bool)
@option("--lnd-krub", is_flag=True, help="Build lnd-krub optional image", type=bool)
@option("--ord-server", is_flag=True, help="Build ord-server optional image", type=bool)
@option("--tesla-ball", is_flag=True, help="Build tesla-ball optional image", type=bool)
def build(
  bitcoind_cat: bool, cashu_mint: bool, lnd_krub: bool, ord_server: bool, tesla_ball: bool
) -> None:
  """Build peripheral images for the desired cluster."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  ### Build optional images ###
  image_names: List[str] = list(
    map(
      lambda image: image.tags[0].split(":")[0],
      filter(lambda image: len(image.tags) != 0, client.images.list()),
    )
  )
  build_select: Dict[str, bool] = {
    "bitcoind-cat": bitcoind_cat,
    "cashu-mint": cashu_mint,
    "lnd-krub": lnd_krub,
    "ord-server": ord_server,
    "tesla-ball": tesla_ball,
  }

  outputs: List[str] = []
  built: Set[str] = {tag for tag in BUILDS.keys() if build_select[tag] and tag in image_names}
  outputs += map(lambda tag: f"<Image: '{tag}'> already exists in local docker images.", built)
  list(map(rich_print, outputs))
  outputs = []

  builds: Dict[str, Build] = {
    tag: build for tag, build in BUILDS.items() if build_select[tag] and tag not in image_names
  }
  if len(builds.keys()) != 0:
    with Progress() as progress:
      builds_items = builds.items()
      task = progress.add_task("Build optional images:".ljust(42), total=len(builds_items))
      for tag, build in builds_items:
        with BytesIO("\n".join(build.instructions).encode("utf-8")) as fileobj:
          try:
            stream = client.api.build(
              decode=True, fileobj=fileobj, platform=build.platform, rm=True, tag=tag
            )
            for line in stream:
              with progress.console.pager(styles=True):
                if "stream" in line:
                  progress.console.print(line.pop("stream").strip(), style="green bold")
                elif "error" in line:
                  progress.console.print(line.pop("error").strip(), style="red bold")
          except BuildError:
            outputs.append(f"[red bold]Build unsuccessful for <Image '{ tag }'>.")
      progress.update(task, description="[blue]Complete", advance=100)
    list(map(rich_print, outputs))


__all__ = ["build"]
