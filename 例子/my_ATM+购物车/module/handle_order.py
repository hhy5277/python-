# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/21 0021
# 获取各种表格接口

import json,os


class Order:
    def __init__(self):
        self.__DB_user = os.path.abspath("DB/DB_table/user.json")

    def ObtainBalance(self,username):
        return self.__getUserInfo(username)["balance"]

    def __getUserInfo(self,username):
        if username:
            with open(self.__DB_user, "r") as f:
                # reads = f.read()
                # if reads == "":
                #     read = {}
                # else:
                #     read = json.loads(reads)
                # for i in read:
                #     if user == i:
                #         return read[i]
                # return False
                userData=json.load(f)
                if username in userData:
                    return userData[username]
                else:
                    return  False
        else:
            return False

