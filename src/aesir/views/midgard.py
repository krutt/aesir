#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/midgard.py
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
from aesir.types import LNDInfo


class Midgard(BaseModel):
  """
  Realm of men, created by Odin and his two brothers Veli and Ve
  """

  model_config = ConfigDict(arbitrary_types_allowed=True)
  container: Container

  @property
  def renderable(self) -> RenderableType:
    lnd_info: LNDInfo = TypeAdapter(LNDInfo).validate_json(
      self.container.exec_run(
        """
        lncli
          --macaroonpath=/root/.lnd/data/chain/bitcoin/regtest/admin.macaroon
          --rpcserver=localhost:10009
          --tlscertpath=/root/.lnd/tls.cert
        getinfo
        """
      ).output
    )
    return Text.assemble(
      "\n\n\n",
      ("Nodekey:\n", "light_coral bold"),
      lnd_info.identity_pubkey,
      "\n",
      "\n".ljust(19),
      ("Channels:".ljust(10), "green bold"),
      str(lnd_info.num_active_channels).rjust(20),
      "\n".ljust(19),
      ("Peers:".ljust(10), "cyan bold"),
      str(lnd_info.num_peers).rjust(20),
      "\n".ljust(19),
      ("Blocks:".ljust(10), "rosy_brown bold"),
      str(lnd_info.block_height).rjust(20),
      "\n".ljust(19),
      ("Synced?:".ljust(10), "steel_blue bold"),
      ("true".rjust(20), "green") if lnd_info.synced_to_chain else ("false".rjust(20), "red"),
      "\n\n\n",
    )


__all__: tuple[str, ...] = ("Midgard",)
