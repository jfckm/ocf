#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *


lib = None

class OcfLib:
    __lib__ = None

    @staticmethod
    def getInstance():
        if (None == OcfLib.__lib__):
            lib = cdll.LoadLibrary('./libocf.so')
            OcfLib()
            __lib__ = lib

        return lib
