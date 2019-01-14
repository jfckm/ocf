/*
 * Copyright(c) 2012-2018 Intel Corporation
 * SPDX-License-Identifier: BSD-3-Clause-Clear
 */
#include <stdio.h>
#include <stdarg.h>
#include "ocf/ocf_logger.h"

int ocf_framework_logger(void *logger,
                ocf_logger_lvl_t lvl, const char *fmt, va_list args)
{
        FILE *lfile = stdout;

        if (lvl > log_info)
                return 0;

        if (lvl <= log_warn)
                lfile = stderr;

        return vfprintf(lfile, fmt, args);
}


