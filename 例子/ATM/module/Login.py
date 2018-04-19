# -*- coding:utf-8 -*-
# AUTHER   @ Alvin
import json
import os
import re
import getpass
from module.Logs import Loggs
from module.Session import Session
from module.Cookies import Cookie
from module.Tshash import Tshash
class Login(object):

    def __init__(self):
        self.__file_path = os.path.abspath("DB/DB_table")
        self.__sep = os.path.sep
        self.__DbUserStatusPath = os.path.abspath("DB/DB_table/userstatus.json")

    ''' 登录 '''
    def __login(self, username, password):
        count = False
        with open(self.__file_path +  self.__sep + "user.json", "r") as f:
            # print(f.read())
            s = json.loads(f.read())
            if username in s:
                if s[username]["password"] == password:
                    count = True
                    Loggs().All("登录成功！")
                    Session()[username] = username
                    # 修改用户状态
                    self.UserStatus(username, status=True)
                    print("登录成功！")
                    return True
                else:
                    Loggs().Error("用户不存在或密码错误！")
                    print("用户名或密码不正确！")
                    return False
            else:
                print("非法用户！！！")
                return False

    ''' 注销 '''
    def loginout(self,username):
        del Cookie()["sessionid"]
        del Session()[username]
        self.UserStatus(username, status=False)
        return True

    ''' 修改用户状态 '''
    def UserStatus(self, username, status = True):
        read = ""
        with open(self.__DbUserStatusPath, "r") as f:
            read = json.loads(f.read())
        if status == True:
            read[username] = {"status" : status, "cookie" : Tshash().Jam_hash("cookie_sessionid")}
        else:
            del read[username]
        with open(self.__DbUserStatusPath, "w") as f:
            json.dump(read, f)
            return True

    ''' 登录，注册接口 '''
    def getLogin(self):
        # print("")
        username = input("用户名：").strip()
        password = input("密码：").strip()
        if re.search("\W+", password) == None and re.search("\W+", username) == None:
            if self.__login(username, Tshash().Jam_hash(password)):
                return True
            else:
                return False
        else:
            print("含有非法字符，用户名和密码只能是字母和数字")
            return False
