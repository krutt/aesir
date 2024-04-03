#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2024 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/pull.py
# VERSION: 	   0.4.1
# CREATED: 	   2023-12-01 06:18
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, List, Set

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import DockerException
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from aesir.configs import IMAGES


@command
@option("--postgres", is_flag=True, help="Pull postgres optional image", type=bool)
@option("--redis", is_flag=True, help="Pull redis optional image", type=bool)
def pull(postgres: bool, redis: bool) -> None:
  """Download required and flagged optional docker images from hub."""
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
  optional_select: Dict[str, bool] = {"postgres": postgres, "redis": redis}
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


__all__ = ["pull"]
