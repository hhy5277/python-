# -*- coding:utf-8 -*-
# AUTHER   @ Alvin
import datetime
import time
import random

# print(time.strftime("%Y",time.time()))

print(int(time.strftime("%Y%m%d%H%M%S",time.localtime())) + random.randint(1000,9999))