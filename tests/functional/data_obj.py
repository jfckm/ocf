#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import ocf_io

OPS_NEW_IO = CFUNCTYPE(c_void_p, c_void_p)
OPS_SUBMIT_IO = CFUNCTYPE(None, POINTER(ocf_io.OcfIo))
OPS_SUBMIT_FLUSH = CFUNCTYPE(None, c_void_p)
OPS_SUBMIT_METADATA = CFUNCTYPE(None, c_void_p)
OPS_SUBMIT_DISCARD = CFUNCTYPE(None, c_void_p)
OPS_SUBMIT_WRITE_ZEROES = CFUNCTYPE(None, c_void_p)
OPS_OPEN = CFUNCTYPE(c_int, c_void_p)
OPS_CLOSE = CFUNCTYPE(None, c_void_p)
OPS_GET_MAX_IO_SIZE = CFUNCTYPE(c_uint, c_void_p)
OPS_GET_LENGTH = CFUNCTYPE(c_uint64, c_void_p)


data_type = {"CACHE": 1,
             "CORE": 2}

class DataObjCaps(Structure):
    #TODO Caps should be bitfield
    _fields_ = [("atomic_writes", c_uint32)]


class DataObjOps(Structure):
    _fields_ = [("submit_io", OPS_SUBMIT_IO),
                ("submit_flush", OPS_SUBMIT_FLUSH),
                ("submit_metadata", OPS_SUBMIT_METADATA),
                ("submit_discard", OPS_SUBMIT_DISCARD),
                ("submit_write_zeroes", OPS_SUBMIT_WRITE_ZEROES),
                ("open", OPS_OPEN),
                ("close", OPS_CLOSE),
                ("get_max_io_size", OPS_GET_MAX_IO_SIZE),
                ("get_length", OPS_GET_LENGTH)]

class DataObjProperties(Structure):
    _fields_ = [("name", c_char_p),
                ("io_priv_size", c_uint32),
                ("dobj_priv_size", c_uint32),
                ("caps", DataObjCaps),
                ("ops", DataObjOps),
                ("io_ops", ocf_io.OcfIoOps)]
