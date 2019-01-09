#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
from ctypes import *
import ocf

LOGGER_OPEN = CFUNCTYPE(c_int, c_void_p)
LOGGER_CLOSE = CFUNCTYPE(None, c_void_p)
# This one is implemented in c (see logger_helper.c file)
# LOGGER_PRINTF = CFUNCTYPE()
LOGGER_PRINTF_RL = CFUNCTYPE(c_int, c_char_p)
LOGGER_DUMP_STACK = CFUNCTYPE(c_int, c_void_p)

class Logger(Structure):
    _fields_ = [("open", LOGGER_OPEN),
                ("close", LOGGER_CLOSE),
                ("printf", c_void_p),
                ("printf_rl", LOGGER_PRINTF_RL),
                ("dump_stack", LOGGER_DUMP_STACK),
                ("priv", c_void_p)]

def CreateLogger():
    lib = ocf.OcfLib.getInstance()
    logger = Logger()
    logger.printf = cast(lib.ocf_framework_logger, c_void_p)

    return logger
