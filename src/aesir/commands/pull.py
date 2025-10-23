#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/commands/pull.py
# VERSION:     0.5.4
# CREATED:     2023-12-01 06:18
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Iterator

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import DockerException
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from aesir.configs import BUILDS, PERIPHERALS
from aesir.types import Image, Service, ServiceName


@command
@option("--postgres", is_flag=True, help="Pull postgres optional image", type=bool)
@option("--redis", is_flag=True, help="Pull redis optional image", type=bool)
def pull(postgres: bool, redis: bool) -> None:
  """Download required and flagged optional docker images from hub."""
  try:
    client: DockerClient = from_env()
    client.ping()
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  ### Pull required images ###
  outputs: list[str] = []
  docker_images: set[str] = {image.tags[0] for image in client.images.list()}
  for registry_id in track(BUILDS.keys(), "Pull buildable images:".ljust(42)):
    if registry_id in docker_images:
      outputs.append(
        f"<[bright_magenta]Image: [green]'{registry_id}'[reset]> already exists in registry."
      )
    else:
      repository, tag = registry_id.split(":")
      client.images.pull(repository=repository, tag=tag)
      outputs.append(f"<[bright_magenta]Image: [green]'{registry_id}'[reset]> downloaded.")
  list(map(rich_print, outputs))

  ### Pull peripheral images ###
  outputs = []
  peripheral_selector: dict[ServiceName, bool] = {
    "aesir-cashu-mint": False,
    "aesir-ord-server": False,
    "aesir-postgres": postgres,
    "aesir-redis": redis,
  }
  peripherals: Iterator[tuple[ServiceName, Service]] = filter(
    lambda service_tuple: peripheral_selector[service_tuple[0]],
    PERIPHERALS.items(),
  )
  for _, peripheral in track(peripherals, "Pull peripherals images flagged:".ljust(42)):
    registry_id: Image = peripheral.image  # type: ignore[no-redef]
    if registry_id in docker_images:
      outputs.append(
        f"<[bright_magenta]Image: [green]'{registry_id}'[reset]> already exists in registry."
      )
    else:
      repository, tag = registry_id.split(":")
      client.images.pull(repository=repository, tag=tag)
      outputs.append(f"<[bright_magenta]Image: [green]'{registry_id}'[reset]> downloaded.")
  list(map(rich_print, outputs))


__all__: tuple[str, ...] = ("pull",)
