#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/types/mutex_option.py
# VERSION:     0.5.1
# CREATED:     2023-12-01 05:31
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, List, Mapping, Tuple

### Third-party packages ###
from click import Context, Option, UsageError


class MutexOption(Option):
  def __init__(self, *args: Any, **kwargs: Any) -> None:
    self.alternatives: List[Any] = kwargs.pop("alternatives")
    assert self.alternatives, "'alternatives' parameter required."
    kwargs["help"] = (
      kwargs.get("help", "") + f"Option is mutually exclusive with {', '.join(self.alternatives)}."
    ).strip()
    super(MutexOption, self).__init__(*args, **kwargs)

  def handle_parse_result(
    self, ctx: Context, opts: Mapping[str, Any], args: List[str]
  ) -> Tuple[Any, List[str]]:
    current_opt: bool = self.name in opts
    for mutex_option in self.alternatives:
      if mutex_option in opts:
        if current_opt:
          raise UsageError(
            f"Illegal usage: '{self.name}' is mutually exclusive with {mutex_option}."
          )
        else:
          self.prompt = None
    return super(MutexOption, self).handle_parse_result(ctx, opts, args)


__all__: Tuple[str, ...] = ("MutexOption",)
