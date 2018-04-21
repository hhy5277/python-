# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/19 0019
from .cookies import Cookie
from .handle_login import Login
from .session import Session


class UserManage(object):
    def __init__(self):
        pass


    def obtain_username(self):
        sessionid = Cookie()["sessionid"]  # cookie __getitem()
        if sessionid:
            return Session()[sessionid]
        else:
            #  登录流程 ：
            print("进入登录流程")
            if Login().user_login():
                sessionid = Cookie()["sessionid"]
                return Session()[sessionid]
            else:
                return False
