#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/configs.py
# VERSION:     0.5.0
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from pathlib import Path
from subprocess import CalledProcessError, run
from typing import Any, Dict, List, Optional

### Standard packages ###
from pydantic import TypeAdapter
from yaml import Loader, load

### Local modules ###
from aesir.types import (
  Build,
  BuildEnum,
  ClusterEnum,
  Connection,
  ImageAlias,
  ImageEnum,
  PeripheralEnum,
  Service,
  ServiceName,
)

### Extract default connection's host and identity ###
HOST: str
IDENTITY: str
try:
  output: str = (
    "["
    + ",".join(
      run(
        [
          "podman",
          "system",
          "connection",
          "list",
          "--format",
          '{"host": "{{.URI}}", "identity": "{{.Identity}}", "default": {{.Default}}}',
        ],
        capture_output=True,
        check=True,
      )
      .stdout.decode("utf-8")
      .rstrip()
      .split("\n")
    )
    + "]"
  )
  connections: List[Connection] = TypeAdapter(List[Connection]).validate_json(output)
  default_connection: Connection = next(filter(lambda connection: connection.default, connections))
  HOST = default_connection.host
  IDENTITY = default_connection.identity
except CalledProcessError:
  HOST = ""
  IDENTITY = ""

### Parse schemas ###
BUILDS: Dict[BuildEnum, Build]
CLUSTERS: Dict[ClusterEnum, Dict[ServiceName, Service]]
IMAGES: Dict[ImageEnum, Dict[ImageAlias, str]]
NETWORK: str
PERIPHERALS: Dict[PeripheralEnum, Dict[ServiceName, Service]]

file_path: Path = Path(__file__).resolve()
with open(str(file_path).replace("configs.py", "schemas.yml"), "rb") as stream:
  schema: Optional[Dict[str, Any]] = load(stream, Loader=Loader)
  if schema:
    BUILDS = TypeAdapter(Dict[BuildEnum, Build]).validate_python(schema["builds"])
    CLUSTERS = TypeAdapter(Dict[ClusterEnum, Dict[ServiceName, Service]]).validate_python(
      schema["clusters"]
    )
    IMAGES = TypeAdapter(Dict[ImageEnum, Dict[ImageAlias, str]]).validate_python(schema["images"])
    NETWORK = schema.get("network", "aesir")
    PERIPHERALS = TypeAdapter(Dict[PeripheralEnum, Dict[ServiceName, Service]]).validate_python(
      schema["peripherals"]
    )

__all__ = ("BUILDS", "CLUSTERS", "IMAGES", "NETWORK", "PERIPHERALS")
