# -*- coding: utf-8 -*-
import os
from django.conf import settings
from logbook import Logger, FileHandler, set_datetime_format


def logger_config(logger_name, log_path):
    """
        根据logger名称和文件位置，封装logger
    :logger_name: string, logger name
    :log_path: log file path with LOG_BASE_DIR e.g:xxx.log
    :return: logger
    """
    log_dir = os.path.join(settings.LOG_BASE_DIR, log_path)
    handler = FileHandler(log_dir)
    handler.push_application()
    logger = Logger(logger_name)
    set_datetime_format('local')
    return logger
