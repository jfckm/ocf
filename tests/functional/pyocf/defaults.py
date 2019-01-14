#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

from ctypes import *
import datetime as dt

from .types.logger import Logger, LogLevel
from .types.queue import Queue
from .types.data import Data
from .types.cleaner import Cleaner
from .types.metadata_updater import MetadataUpdater
from .types.ctx import OcfCtx
from .ocf import OcfLib


class DefaultLogger(Logger):
    def __init__(self, level: LogLevel = LogLevel.WARN):
        super().__init__()
        self.level = level

    def log(self, lvl: int, msg: str):
        if lvl <= self.level:
            print(msg)


class FileLogger(Logger):
    def __init__(self, f, append=False):
        super().__init__()
        self.file = f
        self.mode = "a" if append else "w"

    def open(self):
        try:
            self.f_handle = open(self.file, self.mode, buffering=1)
            return 0
        except:
            raise Exception("Couldn't open log file")

    def close(self):
        close(self.f_handle)

    def log(self, lvl, msg):
        print(
            "{}\t{}\t{}".format(dt.datetime.now(), LogLevel(lvl).name, msg),
            file=self.f_handle,
        )


def get_default_ctx(logger):
    return OcfCtx(
        OcfLib.getInstance(),
        b"PyOCF default ctx",
        logger,
        Data,
        MetadataUpdater,
        Queue,
        Cleaner,
    )
