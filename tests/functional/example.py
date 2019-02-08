#!/usr/bin/python3
#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

from ctypes import *
import pprint

from pyocf.ocf import OcfLib
from pyocf import defaults
from pyocf.types.data import Data
from pyocf.types.data_object import DataObject, ErrorDevice
from pyocf.types.logger import LogLevel
from pyocf.types.cache import Cache
from pyocf.types.core import Core
from pyocf.types.io import IoDir

from pyocf.utils import Size as S, print_structure

# Load Ocf library
lib = OcfLib.getInstance()

c = defaults.get_default_ctx(defaults.DefaultLogger(LogLevel.DEBUG))
c.register_data_object_type(DataObject)
c.register_data_object_type(ErrorDevice)

cache_device = DataObject(200 * 1024 * 1024, "cache_device")
# cache_device = ErrorDevice(200 * 1024 * 1024, set([0]),"cache_device")
# core1_device = ErrorDevice(300 * 1024 * 1024, set([0, 5]), "core1")
core1_device = DataObject(300 * 1024 * 1024, "core1")
core2_device = DataObject(300 * 1024 * 1024, "core2")


cache = Cache.start_on_device(cache_device)
core = Core.using_device(core1_device)
core2 = Core.using_device(core2_device)
cache.add_core(core)

io1 = core.new_core_io()
data1 = Data.from_string("This is MY data")
io1.configure(0, data1.size, IoDir.WRITE, 0, 0)
io1.set_data(data1)
io1.submit()

io2 = core.new_io()
data2 = Data(20)
io2.configure(3, 11, IoDir.READ, 0, 0)
io2.set_data(data2)
print(data2)
io2.submit()
print(data2)
s = cache.get_stats()
pprint.pprint(s)

s = core.get_stats()
pprint.pprint(s)
