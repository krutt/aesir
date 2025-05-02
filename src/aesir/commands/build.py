# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/build.py
# VERSION:     0.5.1
# CREATED:     2024-02-27 23:52
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from io import BytesIO
from typing import Dict, List, Set, Tuple

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import APIError, BuildError
from rich import print as rich_print
from rich.progress import TaskID

### Local modules ###
from aesir.configs import BUILDS
from aesir.types import Build
from aesir.views import Yggdrasil


@command
@option("--bitcoind", is_flag=True, help="Build bitcoind image", type=bool)
@option("--bitcoind-cat", is_flag=True, help="Build bitcoind-cat optional image", type=bool)
@option("--cashu-mint", is_flag=True, help="Build cashu-mint optional image", type=bool)
@option("--lnd", is_flag=True, help="Build lnd image", type=bool)
@option("--lnd-krub", is_flag=True, help="Build lnd-krub optional image", type=bool)
@option("--ord-server", is_flag=True, help="Build ord-server optional image", type=bool)
def build(
  bitcoind: bool,
  bitcoind_cat: bool,
  cashu_mint: bool,
  lnd: bool,
  lnd_krub: bool,
  ord_server: bool,
) -> None:
  """Build peripheral images for the desired cluster."""
  try:
    client: DockerClient = from_env()
    client.ping()
  except APIError:
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
    "bitcoind": bitcoind,
    "bitcoind-cat": bitcoind_cat,
    "cashu-mint": cashu_mint,
    "lnd": lnd,
    "lnd-krub": lnd_krub,
    "ord-server": ord_server,
  }

  outputs: List[str] = []
  built: Set[str] = {tag for tag in BUILDS.keys() if build_select[tag] and tag in image_names}
  outputs += map(lambda tag: f"<Image: '{tag}'> already exists within images.", built)
  list(map(rich_print, outputs))

  builds: Dict[str, Build] = {
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
          except BuildError:
            yggdrasil.update(build_task_id, completed=-1)
            continue
          yggdrasil.update(build_task_id, completed=100)
          yggdrasil.update(task_id, advance=1)
      yggdrasil.update(task_id, completed=build_count, description="[blue]Complete[reset]")


__all__: Tuple[str, ...] = ("build",)
