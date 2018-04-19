# -*- coding:utf-8 -*-
# AUTHER   @ Alvin
import os
import time
import random
import re
from module.Tshash import Tshash
from module.Session import Session
from module.Cookies import Cookie
from module.Login import Login
import json

class User(object):
    ''' 用户管理 '''

    def __init__(self):
        # E:\Python\Python\模块二\homework\ATMofCart\DB_table
        self.__DbPath = os.path.abspath("DB/DB_table/")
        self.__DbUserStatusPath = os.path.abspath("DB/DB_table/userstatus.json")
        self.__DbUserPath = os.path.abspath("DB/DB_table/user.json")
        self.__sep = os.path.sep

    ''' 添加用户 '''
    def AddUser(self, username, password):
        if self.JurisdictionYroN(0):
            read = ""
            with open(self.__DbUserPath, "r") as f:
                read = f.read()
            if username in json.loads(read):
                print("用户名重复！")
                return False
            else:
                with open(self.__DbUserPath, "w") as f:
                    data = json.loads(read)
                    datas = data[username] = {}
                    datas["userid"] = int(time.strftime("%Y%m%d%H%M%S", time.localtime())) + random.randint(1000,9999)
                    datas["username"] = username
                    datas["password"] = Tshash().Jam_hash(str(password))
                    while True:
                        balances = input("初始化金额为：￥5000，是否修改(Y or N)")
                        if balances == "y" or balances == "Y":
                            while True:
                                balanceManey = input("初始化金额：").strip()
                                if re.search("\d+", balanceManey) != None:
                                    datas["balance"] = int(balanceManey)
                                    break
                                else:
                                    print("数据不合法！")
                            break
                        else:
                            datas["balance"] = 5000
                            break
                    datas["status"] = 0
                    datas["userstatus"] = 0
                    datas["loginstatus"] = 1
                    datas["jurisdiction"] = 2
                    json.dump(data, f)
                    return True
        else:
            return False

    ''' 判断当前用户是否有权限做该操作 '''
    def JurisdictionYroN(self, Jurisdiction = 2):
        num = self.AccesstoJurisdictionUser(self.ObtainUsername())
        if num == 0:
            return True
        elif int(num) > 0:
            if int(num) <= int(Jurisdiction):
                return True
            else:
                print("Sorry!无权限操作！")
                return False
        else:
            return False

    ''' 删除用户 '''
    def DelUser(self, user):
        if self.JurisdictionYroN(0):
            read = {}
            with open(self.__DbUserPath, "r") as f:
                read = json.loads(f.read())
            with open(self.__DbUserPath, "w") as f:
                del read[user]
                json.dump(read, f)
                return True
        else:
            return False

    ''' 软删除用户 '''
    def ReUser(self,user):
        if self.JurisdictionYroN(1):
            makeUser = self.MakeUser(username=user, userstatus=1)
            if makeUser:
                return True
            else:
                return False
        else:
            return False

    ''' 恢复用户 '''
    def rReUser(self,user):
        if self.JurisdictionYroN(1):
            makeUser = self.MakeUser(username=user, userstatus=0)
            if makeUser:
                return True
            else:
                return False
        else:
            return False

    ''' 操作过滤 '''
    def MakeUser(self,username=None, password=None, balance=None,status=None,userstatus=None,loginstatus=None,jurisdiction=None):
        if self.JurisdictionYroN(1):
            if username == "root" and self.ObtainUsername() == "root":
                self.__MakeUser(username, password, balance, status,userstatus, loginstatus,jurisdiction)
                return True
            elif username != None:
                self.__MakeUser(username, password, balance, status,userstatus, loginstatus,jurisdiction)
                return True
            else:
                print("无权限操作！")
                return False
        else:
            return False

    ''' 用户操作 '''
    def __MakeUser(self,username=None, password=None, balance=None,status=None,userstatus=None,loginstatus=None,jurisdiction=None):
        read = ""
        with open(self.__DbUserPath, "r") as f:
            read = json.loads(f.read())
        with open(self.__DbUserPath, "w") as f:
            if username != None:
                read[username]["username"] = username
            if password != None:
                read[username]["password"] = Tshash().Jam_hash(str(password))
            if balance != None:
                read[username]["balance"] = balance
            if status != None:
                read[username]["status"] = status
            if userstatus != None:
                read[username]["userstatus"] = userstatus
            if loginstatus != None:
                read[username]["loginstatus"] = loginstatus
            if jurisdiction != None:
                read[username]["jurisdiction"] = jurisdiction
            json.dump(read, f)
            return True

    ''' 冻结用户 '''
    def FrozenUser(self, user):
        makeUser = self.MakeUser(username=user, status=1)
        if makeUser:
            return True
        else:
            return False

    ''' 解冻用户 '''
    def rFrozenUser(self, user):
        makeUser = self.MakeUser(username=user, status=0)
        if makeUser:
            return True
        else:
            return False

    ''' 判断用户权限 '''
    def JurisdictionUser(self, user):
        makeUser = self.MakeUser(username=user, status=1)
        if makeUser:
            return True
        else:
            return False

    ''' 获取用户登录状态操作 '''
    def LoginUser(self):
        login = self.ObtainUsername()
        if login:
            return True
        else:
            return False

    ''' 用户在线状态操作 '''
    def StatuaUser(self, status=True):
        if self.LoginUser():
            read = ""
            with open(self.__DbUserStatusPath, "r") as f:
                read = json.loads(f.read())[self.ObtainUsername()]
            if read["status"] == True:
                return True
            else:
                with open(self.__DbUserStatusPath, "w") as f:
                    read["status"] = True
                    read["cookie"] = Tshash().Jam_hash("cookie_sessionid")
                    json.dump(read, f)
                    return True
        else:
            if self.LoginUser():
                return True
            else:
                return False

    ''' 获取用户权限 '''
    def AccesstoJurisdictionUser(self,user):
        if user != False:
            with open(self.__DbPath + "\\user.json", 'r') as f:
                return json.loads(f.read())[user]["jurisdiction"]
        else:
            return False

    ''' 获取当前用户 '''
    def ObtainUsername(self):
        sessionid = Cookie()["sessionid"]
        if sessionid:
            Login().UserStatus(Session()[sessionid])
            return Session()[sessionid]
        else:
            print("请登录！")
            if Login().getLogin():
                sessionid = Cookie()["sessionid"]
                Login().UserStatus(Session()[sessionid])
                return Session()[sessionid]
            else:
                return False

    ''' 获取所有用户 '''
    def GetUserAll(self, status = "userstatus",  userstatus = 0):
        user = self.ObtainUsername()
        if user:
            uses = []
            with open(self.__DbUserPath, "r") as f:
                read = json.loads(f.read())
            for i in read:
                if user != i:
                    if int(read[i][status]) == int(userstatus):
                        uses.append(i)
            return uses


# print(User().ObtainUsername())
# User().AddUser("egon","root")
# print(User().AccesstoJurisdictionUser("root"))
# User().cd("root")
# print(User().JurisdictionYroN(1))
# User().FrozenUser("admin")
# User().rFrozenUser("admin")
# User().ReUser("admin")
# print(User().StatuaUser())

