#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/setup.py
# VERSION: 	   0.3.3
# CREATED: 	   2023-12-01 06:18
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
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
from docker.errors import BuildError, DockerException, ImageNotFound
from docker.models.images import Image
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from src.configs import BUILDS, IMAGES
from src.types import Build


@command
@option("--with-cashu-mint", is_flag=True, help="Build cashu-mint optional image", type=bool)
@option("--with-lnd-krub", is_flag=True, help="Build lnd-krub optional image", type=bool)
@option("--with-postgres", is_flag=True, help="Pull postgres optional image", type=bool)
@option("--with-redis", is_flag=True, help="Pull redis optional image", type=bool)
@option("--with-tesla-ball", is_flag=True, help="Build tesla-ball optional image", type=bool)
def setup(
  with_cashu_mint: bool,
  with_lnd_krub: bool,
  with_postgres: bool,
  with_redis: bool,
  with_tesla_ball: bool,
) -> None:
  """Download docker images used by command-line interface."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  ### Pull required images ###
  outputs: List[str] = []
  docker_images: Set[str] = {image.tags[0] for image in client.images.list()}
  for registry_id in track(IMAGES["required"].values(), "Pull required images:".ljust(42)):
    if registry_id in docker_images:
      outputs.append(f"<Image: '{ registry_id }'> already exists in local docker images.")
    else:
      repository, tag = registry_id.split(":")
      client.images.pull(repository=repository, tag=tag)
      outputs.append(f"<Image: '{ registry_id }'> downloaded.")
  list(map(rich_print, outputs))

  ### Pull optional images ###
  optional_select: Dict[str, bool] = {"postgres": with_postgres, "redis": with_redis}
  optionals: List[str] = [
    registry for alias, registry in IMAGES["optional"].items() if optional_select[alias]
  ]
  if len(optionals) != 0:
    outputs = []
    for registry_id in track(optionals, "Pull optional images flagged:".ljust(42)):
      if registry_id in docker_images:
        outputs.append(f"<Image: '{ registry_id }'> already exists in local docker images.")
      else:
        repository, tag = registry_id.split(":")
        client.images.pull(repository=repository, tag=tag)
        outputs.append(f"<Image: '{ registry_id }'> downloaded.")
    list(map(rich_print, outputs))

  ### Build optional images ###
  build_select: Dict[str, bool] = {
    "cashu-mint": with_cashu_mint,
    "lnd-krub": with_lnd_krub,
    "tesla-ball": with_tesla_ball,
  }
  builds: Dict[str, Build] = {tag: build for tag, build in BUILDS.items() if build_select[tag]}
  if len(builds.keys()) != 0:
    outputs = []
    for tag, build in track(builds.items(), description="Build optional images:".ljust(42)):
      existed: bool = True
      try:
        image: Image = client.images.get(tag)
        outputs.append(f"[dim yellow1]<Image '{ image.tag }'> already exists.>")
      except ImageNotFound:
        existed = False
      if existed:
        continue
      with BytesIO("\n".join(build.instructions).encode("utf-8")) as fileobj:
        try:
          client.images.build(fileobj=fileobj, platform=build.platform, tag=tag)
        except BuildError:
          outputs.append(f"[red bold]Build unsuccessful for <Image '{ tag }'>.")
    list(map(rich_print, outputs))


__all__ = ["setup"]
