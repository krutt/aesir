#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/alfheim.py
# VERSION:     0.5.2
# CREATED:     2025-10-03 13:00
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from docker.models.containers import Container
from pydantic import BaseModel, ConfigDict, TypeAdapter
from rich.console import RenderableType
from rich.text import Text

### Local modules ###
from aesir.types import ElectrsFeatures, JsonrpcResponse


class Alfheim(BaseModel):
  """
  Realm of the Light Elves. Alfheim is another heavenly world, ruled over by Freyr,
  the twin brother of Freya and another of the Vanir gods.
  """

  model_config = ConfigDict(arbitrary_types_allowed=True)
  container: Container

  @property
  def renderable(self) -> RenderableType:
    features: JsonrpcResponse[ElectrsFeatures] = TypeAdapter(
      JsonrpcResponse[ElectrsFeatures]
    ).validate_json(
      self.container.exec_run(
        [
          "sh",
          "-c",
          """
        echo '{"id": "feat", "jsonrpc": "2.0", "method": "server.features"}' | nc -N localhost 50001
        """,
        ]
      ).output
    )
    return Text.assemble(
      "\n\n\n",
      ("Genesis Hash:".ljust(15), "green bold"),
      features.result.genesis_hash,
      "\n\n".ljust(20),
      ("Hash function:".ljust(16), "cyan bold"),
      f"{features.result.hash_function}".rjust(14),
      "\n".ljust(19),
      ("Pruning?:".ljust(15), "bright_magenta bold"),
      ("true".rjust(15), "green") if features.result.pruning else ("false".rjust(15), "red"),
      "\n".ljust(19),
      ("Protocol Minimum:".ljust(13), "light_coral bold"),
      f"{features.result.protocol_min}".rjust(13),
      "\n".ljust(19),
      ("Protocol Maximum:".ljust(13), "blue bold"),
      f"{features.result.protocol_max}".rjust(13),
      "\n\n\n",
    )


__all__: tuple[str, ...] = ("Alfheim",)
