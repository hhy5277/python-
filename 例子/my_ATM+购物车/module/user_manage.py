# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/19 0019
from .cookies import Cookie


class UserManage(object):
    def __init__(self):
        pass

    '''从cookie中取出（判断是否有效）sessionid的值;如果不存在则登录
       如果存在则用sessionid在DB_session（判断是否有效）中取出用户的用户名
       再用用户面去user.json中获取用户的所有信息
    '''
    def obtain_username(self):
        sessionid = Cookie()["sessionid"]
        print(sessionid, "sessionid")
