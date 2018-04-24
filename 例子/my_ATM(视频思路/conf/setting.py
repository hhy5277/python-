# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/15 0015
import os
import logging

# 入口文件目录 也是项目的的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "accounts")

TRANSACTION_TYPE = {
    "with_draw": {"action": "minus", "interest": 0.05},
    "repay": {"action": "plus", "interest": 0.0}
}
