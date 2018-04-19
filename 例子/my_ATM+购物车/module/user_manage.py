# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/19 0019
from .cookies import Cookie

class UserManage(object):
    def __init__(self):
        pass

    def obtain_username(self):
        sessionid = Cookie()["sessionid"]
        print(sessionid,"sessionid")

