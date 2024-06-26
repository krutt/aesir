#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/build.py
# VERSION:     0.4.5
# CREATED:     2024-02-27 23:52
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from io import BytesIO
from math import floor
from re import search
from typing import Dict, List, Set

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import BuildError, DockerException
from rich import print as rich_print

### Local modules ###
from aesir.configs import BUILDS
from aesir.types import Build
from aesir.views import Yggdrasil


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

  builds: Dict[str, Build] = {
    tag: build for tag, build in BUILDS.items() if build_select[tag] and tag not in image_names
  }
  build_count: int = len(builds.keys())
  if build_count != 0:
    with Yggdrasil(row_count=10) as yggdrasil:
      builds_items = builds.items()
      task = yggdrasil.add_task("Build specified images:".ljust(42), total=build_count)
      for tag, build in builds_items:
        build_task = yggdrasil.add_task(
          f"Building <[bright_magenta]Image [green]'{tag}'[reset]>…".ljust(42), total=100
        )
        with BytesIO("\n".join(build.instructions).encode("utf-8")) as fileobj:
          try:
            chunk = client.api.build(
              decode=True, fileobj=fileobj, platform=build.platform, rm=True, tag=tag
            )
            for line in chunk:
              if "stream" in line:
                stream: str = line.pop("stream").strip()
                step = search(r"^Step (?P<divided>\d+)\/(?P<divisor>\d+) :", stream)
                if step is not None:
                  divided: int = int(step.group("divided"))
                  divisor: int = int(step.group("divisor"))
                  yggdrasil.update(build_task, completed=floor(divided / divisor * 100))
                yggdrasil.update_table(stream)
              elif "error" in line:
                yggdrasil.update_table(line.pop("error").strip())
          except BuildError:
            yggdrasil.update(
              build_task,
              completed=0,
              description=f"[red bold]Build unsuccessful for <Image '{tag}'>.",
            )
          yggdrasil.update(
            build_task,
            completed=100,
            description=f"[blue]Built <[bright_magenta]Image [green]'{tag}'[reset]> successfully.",
          )
          yggdrasil.update(task, advance=1)
      yggdrasil.update(task, completed=build_count, description="[blue]Complete")


__all__ = ("build",)
