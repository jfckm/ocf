#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import ocf_io
import io_utils
import ocf
import context_ops


lib = ocf.OcfLib.getInstance()
lib.ocf_io_get_priv.restype = POINTER(io_utils.DataObjIo)

@CFUNCTYPE(c_int, POINTER(ocf_io.OcfIo), c_void_p, c_uint32)
def io_set_data(io, data, offset):
    dobj_io = lib.ocf_io_get_priv(io)
    dobj_io.contents.data = data

    return 0


@CFUNCTYPE(c_void_p, POINTER(ocf_io.OcfIo))
def io_get_data(io):
    dobj_io = lib.ocf_io_get_priv(io)
    dobj_data = dobj_io.contents.data

    return dobj_data

