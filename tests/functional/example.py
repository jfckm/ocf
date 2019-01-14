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
from pyocf.types.data_object import DataObject
from pyocf.types.logger import LogLevel
from pyocf.types.cache import Cache
from pyocf.types.core import Core
from pyocf.types.io import IoDir

from pyocf.utils import Size as S, print_structure

# Load Ocf library
lib = OcfLib.getInstance()

c = defaults.get_default_ctx(defaults.DefaultLogger(LogLevel.DEBUG))
c.register_data_object_type(DataObject)
d1 = DataObject(200 * 1024 * 1024, "data1")
d2 = DataObject(300 * 1024 * 1024, "data2")

d3 = DataObject(300 * 1024 * 1024, "data3")
cache = Cache.using_device(d1)
core = Core.using_device(d2)
core2 = Core.using_device(d3)
cache.add_core(core)
cache.add_core(core2)

io1 = core.new_io()
data1 = Data.from_string("This is MY data")
io1.configure(0, data1.size, IoDir.WRITE, 0, 0)
io1.set_data(data1)
io1.submit()

io1 = core2.new_io()
io1.configure(8, data1.size, IoDir.WRITE, 0, 0)
io1.set_data(data1)
io1.submit()

io1.del_object()

io2 = core.new_io()
data2 = Data(20)
io2.configure(3, 11, IoDir.READ, 0, 0)
io2.set_data(data2)
print(data2)
io2.submit()
print(data2)

io2.del_object()

d1.dump_contents(stop_after_zeros=20000)
s = cache.get_stats()
pprint.pprint(s)

print_structure(s["usage"])
