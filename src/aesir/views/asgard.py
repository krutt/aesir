#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/asgard.py
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
from rich.console import Group, RenderableType
from rich.rule import Rule
from rich.text import Text

### Local modules ###
from aesir.types import BlockchainInfo, MempoolInfo


class Asgard(BaseModel):
  """
  Homeland of the Aesir gods. Asgard lies in the middle of the sky, also on the top of Yggdrasil.
  """

  model_config = ConfigDict(arbitrary_types_allowed=True)
  container: Container

  @property
  def renderable(self) -> RenderableType:
    blockchain_info: BlockchainInfo = TypeAdapter(BlockchainInfo).validate_json(
      self.container.exec_run(
        """
        bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir getblockchaininfo
        """
      ).output
    )
    mempool_info: MempoolInfo = TypeAdapter(MempoolInfo).validate_json(
      self.container.exec_run(
        """
        bitcoin-cli -regtest -rpcuser=aesir -rpcpassword=aesir getmempoolinfo
        """
      ).output
    )
    return Group(
      Text.assemble(
        f"\n{'Blockchain information:'.ljust(20)}\n",
        ("Chain: ", "bright_magenta bold"),
        blockchain_info.chain.ljust(9),
        ("Blocks: ", "green bold"),
        f"{blockchain_info.blocks}".ljust(8),
        ("Size: ", "blue bold"),
        f"{blockchain_info.size_on_disk}".ljust(10),
        ("Time: ", "cyan bold"),
        f"{blockchain_info.time}".rjust(10),
        "\n",
      ),
      Rule(),
      Text.assemble(
        "\n",
        ("Mempool information:".ljust(19), "bold"),
        "\n".ljust(19),
        ("Fees:".ljust(15), "green bold"),
        f"{mempool_info.total_fee}".rjust(15),
        "\n".ljust(19),
        ("Transactions:".ljust(15), "cyan bold"),
        f"{mempool_info.txn_count}".rjust(15),
        "\n".ljust(19),
        ("Size:".ljust(15), "blue bold"),
        f"{mempool_info.txn_bytes}".rjust(15),
        "\n".ljust(19),
        ("Loaded?:".ljust(15), "bright_magenta bold"),
        ("true".rjust(15), "green") if mempool_info.loaded else ("false".rjust(15), "red"),
        "\n".ljust(19),
        ("Usage:".ljust(15), "light_coral bold"),
        f"{mempool_info.usage}".rjust(15),
        "\n",
      ),
    )


__all__: tuple[str, ...] = ("Asgard",)
