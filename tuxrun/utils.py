# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
import sys


class ProgressIndicator(ABC):
    @abstractmethod
    def progress(self, percent):
        """
        This method should display the current percentage to the user
        """

    @abstractmethod
    def finish(self):
        """
        This method should display to the user that the process has finished
        """


class NoProgressIndicator(ProgressIndicator):
    def progress(self, percent):
        pass

    def finish(self):
        pass


class TTYProgressIndicator(ProgressIndicator):
    def __init__(self, name):
        self.name = name
        self.first_message = False

    def progress(self, percent: int) -> None:
        if sys.stderr.isatty():
            sys.stderr.write(f"\r{self.name} ... %3d%%" % percent)
        elif self.first_message:
            sys.stderr.write(f"\r{self.name}\n")
            self.first_message = False

    def finish(self) -> None:
        if sys.stderr.isatty():
            sys.stderr.write("\n")
