# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/5/1 0001

import os,sys

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
if __name__ =="__main__":
    from core import management
    # 首先解析用户的参数  单独写一个management类进行处理
    argv_parser = management.ManagementTool(sys.argv)
    argv_parser.execute()

