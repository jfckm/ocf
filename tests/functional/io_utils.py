#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import ocf
from ocf_io import *


lib = ocf.OcfLib.getInstance()
lib.ocf_core_new_io_wrapper.restype = POINTER(OcfIo)
lib.ocf_io_set_cmpl_wrapper.argtypes = [POINTER(OcfIo), c_void_p, c_void_p,
                                                IO_END]
lib.ocf_io_configure_wrapper.argtypes = [POINTER(OcfIo), c_uint64, c_uint32,
                                              c_uint32, c_uint32, c_uint64]
lib.ocf_io_set_queue_wrapper.argtypes = [POINTER(OcfIo), c_uint32]

class DataObjIo(Structure):
    _fields_ = [("data", c_void_p),
                ("offset", c_uint64)]

    def __init__(self, size):
        self.data = cast((c_byte * size)(), c_void_p)
        self.offset = 0


class Data(Structure):
    _fields_ = [("data", c_void_p)]

    def __init__(self, pages=1):
        self.data = cast(create_string_buffer(4096 * pages), c_void_p)


def check_ret_val(ret):
    if (0 != ret):
        print ("Error: ", ret)
        exit(ret)


@CFUNCTYPE(None, POINTER(OcfIo), c_int)
def simple_completion(io, err):
    if (0 != err):
        print("Io completion error: ", err)


def io(dir, addr, data, bytes, core_obj, cmpl_fn, io_class=0, flags=0):
    io = lib.ocf_core_new_io_wrapper(core_obj)
    if (0 == io):
        print("io alloc failed in new_io")
        exit(1)
    lib.ocf_io_configure_wrapper(io, addr, bytes, dir, io_class, flags)
    ret = lib.ocf_io_set_data_wrapper(io, byref(data), 0)
    lib.ocf_io_set_cmpl_wrapper(io, 0, 0, cmpl_fn)
    lib.ocf_io_set_queue_wrapper(io, 0)

    ret = lib.ocf_core_submit_io_wrapper(io)
    check_ret_val(ret)


def read(addr, data, bytes, core_obj, cmpl_fn):
    return io(dir["READ"], addr, data, bytes, core_obj, cmpl_fn)

def write(addr, data, bytes, core_obj, cmpl_fn):
    return io(dir["WRITE"], addr, data, bytes, core_obj, cmpl_fn)

