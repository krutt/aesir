#!/usr/bin/env python3.10
# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/exceptions.py
# VERSION:     0.5.4
# CREATED:     2025-05-05 01:23
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************


class BuildUnsuccessful(OSError):
  def __init__(self, code: int, message: str):
    self.errno = code
    self.strerr = message


__all__: tuple[str, ...] = ("BuildUnsuccessful",)
