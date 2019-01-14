#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

from ctypes import *
from enum import IntEnum

from ..ocf import OcfLib
from .data import Data
from .shared import SharedOcfObject


class IoDir(IntEnum):
    READ = (0,)
    WRITE = 1


class IoOps(Structure):
    pass


class Io(Structure):
    START = CFUNCTYPE(None, c_void_p)
    HANDLE = CFUNCTYPE(None, c_void_p, c_void_p)
    END = CFUNCTYPE(None, c_void_p, c_int)

    _instances_ = {}
    _fields_ = [
        ("_obj", c_void_p),
        ("_ops", POINTER(IoOps)),
        ("_addr", c_uint64),
        ("_flags", c_uint64),
        ("_bytes", c_uint32),
        ("_class", c_uint32),
        ("_dir", c_uint32),
        ("_io_queue", c_uint32),
        ("_start", START),
        ("_handle", HANDLE),
        ("_end", END),
        ("_priv1", c_void_p),
        ("_priv2", c_void_p),
    ]

    @classmethod
    def from_pointer(cls, ref):
        c = cls.from_address(ref)
        cls._instances_[ref] = c
        OcfLib.getInstance().ocf_io_set_cmpl_wrapper(byref(c), None, None, c.c_end)
        return c

    @classmethod
    def get_instance(cls, ref):
        return cls._instances_[cast(ref, c_void_p).value]

    def del_object(self):
        try:
            del type(self)._instances_[cast(byref(self), c_void_p).value]
        except:
            pass

    def __del__(self):
        self.del_object()

    @staticmethod
    @END
    def c_end(io, err):
        Io.get_instance(io).end(err)

    @staticmethod
    @START
    def c_start(io):
        Io.get_instance(io).start()

    @staticmethod
    @HANDLE
    def c_handle(io, opaque):
        Io.get_instance(io).handle(opaque)

    def end(self, err):
        if err:
            print("IO err {}".format(err))

    def submit(self):
        return OcfLib.getInstance().ocf_core_submit_io_wrapper(byref(self))

    def configure(
        self, addr: int, length: int, direction: IoDir, io_class: int, flags: int
    ):
        OcfLib.getInstance().ocf_io_configure_wrapper(
            byref(self), addr, length, direction, io_class, flags
        )

    def set_data(self, data: Data):
        result = OcfLib.getInstance().ocf_io_set_data_wrapper(byref(self), data, 0)


IoOps.SET_DATA = CFUNCTYPE(c_int, POINTER(Io), c_void_p, c_uint32)
IoOps.GET_DATA = CFUNCTYPE(c_void_p, POINTER(Io))

IoOps._fields_ = [("_set_data", IoOps.SET_DATA), ("_get_data", IoOps.GET_DATA)]

lib = OcfLib.getInstance()
lib.ocf_core_new_io_wrapper.restype = POINTER(Io)
lib.ocf_io_set_cmpl_wrapper.argtypes = [POINTER(Io), c_void_p, c_void_p, Io.END]
lib.ocf_io_configure_wrapper.argtypes = [
    POINTER(Io),
    c_uint64,
    c_uint32,
    c_uint32,
    c_uint32,
    c_uint64,
]
lib.ocf_io_set_queue_wrapper.argtypes = [POINTER(Io), c_uint32]

lib.ocf_core_new_io_wrapper.argtypes = [c_void_p]
lib.ocf_core_new_io_wrapper.restype = c_void_p

lib.ocf_io_set_data_wrapper.argtypres = [POINTER(Io), c_void_p, c_uint32]
lib.ocf_io_set_data_wrapper.restype = c_int
