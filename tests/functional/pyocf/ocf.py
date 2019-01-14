#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *

lib = None


class OcfLib:
    __lib__ = None

    @classmethod
    def getInstance(cls):
        if None == cls.__lib__:
            lib = cdll.LoadLibrary("./pyocf/libocf.so")
            lib.ocf_dobj_get_uuid.restype = c_void_p
            lib.ocf_dobj_get_uuid.argtypes = [c_void_p]

            lib.ocf_core_get_front_data_object.restype = c_void_p
            lib.ocf_core_get_front_data_object.argtypes = [c_void_p]

            cls.__lib__ = lib

        return cls.__lib__
