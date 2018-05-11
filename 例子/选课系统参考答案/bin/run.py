#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Henson

import os
import sys
import platform

#判断平台是win还是linux
if platform.system() == 'Windows':
    BASE_DIR = "\\".join(os.path.abspath(os.path.dirname(__file__)).split("\\")[:-1])
else:
    BASE_DIR = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
sys.path.insert(0, BASE_DIR)

from core import main

if __name__ == '__main__':
    main.run()