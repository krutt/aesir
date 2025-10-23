#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/views/helheim.py
# VERSION:     0.5.2
# CREATED:     2025-10-23 18:59
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from docker.models.containers import Container
from pydantic import BaseModel, ConfigDict, TypeAdapter
from rich.console import RenderableType
from rich.console import Group
from rich.rule import Rule
from rich.text import Text

### Local modules ###
from aesir.types import LitdInfo, LitdStatus


class Helheim(BaseModel):
  """
  Realm of the Light Elves. Alfheim is another heavenly world, ruled over by Freyr,
  the twin brother of Freya and another of the Vanir gods.
  """

  model_config = ConfigDict(arbitrary_types_allowed=True)
  container: Container

  @property
  def renderable(self) -> RenderableType:
    litd_info: LitdInfo = TypeAdapter(LitdInfo).validate_json(
      self.container.exec_run(
        """
        litcli --network=regtest getinfo
        """
      ).output
    )
    litd_status: LitdStatus = TypeAdapter(LitdStatus).validate_json(
      self.container.exec_run(
        """
        litcli --network=regtest status
        """
      ).output.replace(b"}\n{", b",")
    )
    return Group(
      Text.assemble(
        "\n".ljust(19),
        ("Version:".ljust(11), "steel_blue bold"),
        f"{litd_info.version}".rjust(19),
        "\n".ljust(14),
        ("Commit hash:", "light_coral bold"),
        "\n".ljust(14),
        litd_info.commit_hash,
        "\n",
      ),
      Rule(),
      Text.assemble(
        "".rjust(18),
        ("Accounts?:".ljust(15), "bright_magenta bold"),
        ("true".rjust(15), "green")
        if litd_status.sub_servers.accounts.running
        else ("false".rjust(15), "red"),
        "\n".ljust(19),
        ("Faraday?:".ljust(15), "hot_pink bold"),
        ("true".rjust(15), "green")
        if litd_status.sub_servers.faraday.running
        else ("false".rjust(15), "red"),
        "\n".ljust(19),
        ("Lit?:".ljust(15), "light_coral bold"),
        ("true".rjust(15), "green")
        if litd_status.sub_servers.lit.running
        else ("false".rjust(15), "red"),
        "\n".ljust(19),
        ("Lnd?:".ljust(15), "blue bold"),
        ("true".rjust(15), "green")
        if litd_status.sub_servers.lnd.running
        else ("false".rjust(15), "red"),
        "\n".ljust(19),
        ("Loop?:".ljust(15), "sandy_brown bold"),
        ("true".rjust(15), "green")
        if litd_status.sub_servers.loop.running
        else ("false".rjust(15), "red"),
        "\n".ljust(19),
        ("Pool?:".ljust(15), "light_slate_gray bold"),
        ("true".rjust(15), "green")
        if litd_status.sub_servers.pool.running
        else ("false".rjust(15), "red"),
        "\n".ljust(19),
        ("TaprootAssets?:".ljust(15), "rosy_brown bold"),
        ("true".rjust(15), "green")
        if litd_status.sub_servers.taproot_assets.running
        else ("false".rjust(15), "red"),
      ),
    )


__all__: tuple[str, ...] = ("Helheim",)
