# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/19 0019
from .cookies import Cookie
from .handle_login import Login


class UserManage(object):
    def __init__(self):
        pass

    '''从cookie中取出（判断是否有效）sessionid的值;如果不存在则登录
       如果存在则用sessionid在DB_session（判断是否有效）中取出用户的用户名
       再用用户面去user.json中获取用户的所有信息
    '''

    def obtain_username(self):
        sessionid = Cookie()["sessionid"]  # cookie __getitem()
        print(sessionid, "sessionid")
        # if sessionid:
        #     Login().UserStatus(Session()[sessionid])
        #     return Session()[sessionid]
        # else:
        #     print("请登录！")
        #     if Login().getLogin():
        #         sessionid = Cookie()["sessionid"]
        #         Login().UserStatus(Session()[sessionid])
        #         return Session()[sessionid]
        #     else:
        #         return False

        '''
            如果sessionid存在 则用sessionid在Session()中取出用户名
            如果不存在则进入登录流程
        '''
        if sessionid:
            pass
        else:
            #  登录流程 ：
            print("进入登录流程")
            Login().user_login()
