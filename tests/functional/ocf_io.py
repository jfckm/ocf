#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import data_obj


dir = {"READ": 0,
       "WRITE": 1}

class OcfIoOps(Structure):
    pass


class OcfIo(Structure):
    pass

IO_START = CFUNCTYPE(None, POINTER(OcfIo))
IO_HANDLE = CFUNCTYPE(None, POINTER(OcfIo), c_void_p)
IO_END = CFUNCTYPE(None, POINTER(OcfIo), c_int)

#TODO data_obj type
OcfIo._fields_ = [("obj", c_void_p),
                ("ops", POINTER(OcfIoOps)),
                ("addr", c_uint64),
                ("flags", c_uint64),
                ("bytes", c_uint32),
                ("class", c_uint32),
                ("dir", c_uint32),
                ("io_queue", c_uint32),
                ("start", IO_START),
                ("handle", IO_HANDLE),
                ("end", IO_END),
                ("priv1", c_void_p),
                ("priv2", c_void_p)
               ]


IO_SET_DATA = CFUNCTYPE(c_int, POINTER(OcfIo), c_void_p, c_uint32)
IO_GET_DATA = CFUNCTYPE(c_void_p, POINTER(OcfIo))

OcfIoOps. _fields_ = [("set_data", IO_SET_DATA),
                      ("get_data", IO_GET_DATA),
                     ]

