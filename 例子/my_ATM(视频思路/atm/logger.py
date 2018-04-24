# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/16 0016

import logging
from conf import setting
import os

# 日志的类型及对应生成的日子文件名称
LOG_TYPES = {
    "access": "access.log",
    "transaction": "transaction.log"
}
# 日志等级
LOG_LEVEL = logging.INFO
LOG_FORMATTER = logging.Formatter("时间【%(asctime)s】 - 操作名称【%(name)s】 - 级别【%(levelname)s】 - 信息【%(message)s】")


def create_logger(logger_name):
    # 创建一个日志并起名、设置日志等级
    logger = logging.getLogger(logger_name)
    logger.setLevel(LOG_LEVEL)

    # 创建一个默认的console handler、并设置handler等级
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)

    # 通过logger_name 生成一个路径创建一个file handler,并设置等级
    log_file_path = os.path.join(setting.BASE_DIR, "logs", LOG_TYPES[logger_name])
    fh = logging.FileHandler(log_file_path, encoding="utf-8")
    fh.setLevel(LOG_LEVEL)

    # #设置一个日志formatter函数
    # formatter = logging.Formatter(LOG_FORMATTER)

    # add formatter to ch and fh
    ch.setFormatter(LOG_FORMATTER)
    fh.setFormatter(LOG_FORMATTER)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


access_log = create_logger("access")
transaction_log = create_logger("transaction")
