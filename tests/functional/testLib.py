#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import ocf
import test_data_obj as dobj
import context
import cache
import core
from ocf_io import *
import io_utils as io

# Load Ocf library
lib = ocf.OcfLib.getInstance()

# Initialize context
context.InitCtx()

# Register data types
dobj.register_data_obj_types()

# Start cache instance and attach device
cache_obj = cache.start_cache(cache.cache_mode["wt"])

# Add core
core_obj = c_void_p()
core.add_core(cache_obj, core_obj)

# Perform simply write/read IO
io_offset = 0
test_str = b'Litwo! Ojczyzno moja! ty jestes jak zdrowie'
data_len = len(test_str)
write_data = io.Data()
write_data.data = cast(test_str, c_void_p)

# Actual write
io.write(io_offset, write_data, data_len, core_obj, io.simple_completion)

write_data_ptr = cast(write_data.data, c_char_p)
print("Data written: ", write_data_ptr.value)

read_data = io.Data()
read_buff_ptr = cast(read_data.data, c_char_p)
print("Data before read: ", read_buff_ptr.value)

# Actual read
io.read(io_offset, read_data, data_len, core_obj, io.simple_completion)
print("Data after read: ", read_buff_ptr.value)

# print ("cache storage: ")
# dobj.print_storage_buff(dobj.cache_storage)

# print ("core storage: ")
# dobj.print_storage_buff(dobj.core_storage)

print ("Clean exit from python OCF-test-adapter framework!")
lib.ocf_ctx_exit(context.ctx)
