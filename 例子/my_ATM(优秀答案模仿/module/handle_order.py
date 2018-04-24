# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/21 0021
# 获取各种表格接口

import json,os
from .user_manage import UserManage


class Order:
    def __init__(self):
        self.__DB_user = os.path.abspath("DB/DB_table/user.json")

    def ObtainBalance(self,username):
        return self.__getUserData(username)["balance"]

    def __getUserData(self,username):
        if username:
            with open(self.__DB_user, "r") as f:
                userData=json.load(f)
                if username in userData:
                    return userData[username]
                else:
                    return  False
        else:
            return False

    ''' 获取当前用户名称 '''

    def __obtain_username(self):
        user = UserManage().obtain_username()
        if user:
            return user
        else:
            return False


    """username账号是否可使用"""
    def account_is_available(self,tousername):
        user = self.__getUserData(self.__obtain_username())
        toUser =self.__getUserData(tousername)

        userStatus = user["status"]
        toUserStatus =toUser["status"]

        if int(userStatus) != 0:
            print("您的账户被冻结，不能进行该操作！")
            return False
        if int(toUserStatus) != 0:
            print("对方账户被冻结，不能进行该操作！")
            return False
        else:
            return True

    ''' 转账 
            balance：金额
            to：交易对象
            rate：费率
            reason：备注
            operation：操作方式  3转账   1还款
        '''
    def transferAccount(self,balance,to,rate,reason="",operation="3"):
        user=self.__obtain_username()
        money = 0
        service = 0
        if user:
            #判断双方账户是否可用
            if self.account_is_available(to):
                if int(operation)==3: #转账
                    service = self.ServiceCharge(float(balance), float(rate))
                    money = float(balance) - float(service)
                elif int(operation) == 1: #还款
                    money = float(balance)
                    service = float(self.ServiceCharge(balance, rate))


                if float(self.ObtainBalance(user)) >= float(balance):
                    A = self.ChangeUserBalance(user=user, menoy=money)
                    B = self.ChangeUserBalance(user=to, menoy=money, mode="+")
                    if A and B:
                        return True
                    else:
                        print("付款操作失败")
                        return False
                    #开始转账
                else:
                    print("转账失败，您的账户余额不够")
                    return False
            else:
                return False
        else:
            return False

    ''' 处理手续费 
                menoy：交易金额
                rate：费率
        '''

    def ServiceCharge(self, menoy, rate):
        if float(rate) == 0.0:
            return 0
        else:
            return float(menoy) * float(rate)

    ''' 修改用户账户余额 
            user：交易对象
            menoy：金额
            mode：交易方式
    '''
    def ChangeUserBalance(self,user,menoy, mode = "-"):
        with open(self.__DB_user, "r") as f:
            users = json.loads(f.read())

        if mode == "-":
            users[user]["balance"] = float(users[user]["balance"]) - float(menoy)
        else:
            users[user]["balance"] = float(users[user]["balance"]) + float(menoy)
        with open(self.__DB_user, "w") as f:
            json.dump(users,f)
            return True
