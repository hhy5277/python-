# -*- coding:utf-8 -*-
# AUTHER   @ Alvin
import os
import json
import time
import random
from module.Tshash import Tshash
from module.User import User
from module.Logs import Loggs
from module.Carts import Cart
class Order(object):

    def __init__(self):
        self.__DB_order = os.path.abspath("DB/DB_table/order.json")
        self.__DB_user = os.path.abspath("DB/DB_table/user.json")
        self.__DB_Goods = os.path.abspath("DB/DB_table/goods.json")

    ''' 获取余额 
            user：当前用户
    '''
    def ObtainBalance(self, user):
        return self.__GetUser(user)["balance"]

    ''' order表读操作 '''
    def __ReadOrder(self):
        with open(self.__DB_order, "r") as f:
            read = f.read()
            if read == "":
                return {}
            else:
                return json.loads(read)

    ''' order表写操作 
            order：订单表数据
    '''
    def __WriteOrder(self, order):
        with open(self.__DB_order, "w") as f:
            json.dump(order, f)
            return True

    ''' 商品表读操作 '''
    def __ReadGoods(self):
        with open(self.__DB_Goods, "r") as f:
            read = f.read()
            if read == "":
                return {}
            else:
                return json.loads(read)

    ''' 商品表写操作 
            goods：商品表信息
    '''
    def __WriteGoods(self, goods):
        # print(goods)
        with open(self.__DB_Goods, "w") as f:
            json.dump(goods, f)
            return True

    ''' 获取当前用户信息 user：当前用户名称'''
    def __GetUser(self, user):
        if user:
            with open(self.__DB_user, "r") as f:
                reads = f.read()
                if reads == "":
                    read = {}
                else:
                    read = json.loads(reads)
                for i in read:
                    if user == i:
                        return read[i]
                return False
        else:
            return False

    ''' 获取当前用户名称 '''
    def __ObtainUser(self):
        user = User().ObtainUsername()
        if user:
            return user
        else:
            return False

    ''' 还款接口
        money：还款金额
    '''
    def Repayment(self, menoy):
        rate = 0.0005
        if self.__ObtainUser():
            ServiceCharge = float(self.ServiceCharge(menoy, rate))
            ActualAccount = ServiceCharge + float(menoy)
            if self.TransferAccounts(float(ActualAccount), "root", rate, "还款",operation=1):
                if self.__ModifyOrderInformation(float(menoy), "root", ActualAccount, ServiceCharge, 1,"还款", 0.005):
                    print("还款成功！")
                    return True
                else:
                    print("还款失败！")
                    return False
            else:
                print("还款失败！")
                return False
        else:

            return False

    ''' 转账 
        balance：金额
        to：交易对象
        rate：费率
        reason：备注
        operation：操作方式
    '''
    def TransferAccounts(self ,balance, to, rate=0.0005, reason="",operation=3):
        user = self.__ObtainUser()
        money = 0
        service = 0
        if user:
            userStatus = self.__ControlStatus(to)
            if userStatus:
                if int(operation) == 3: #默认转账
                    service = self.ServiceCharge(float(balance), float(rate))
                    money = float(balance) - float(service)
                elif int(operation) == 1: #还款
                    money = float(balance)
                    service = float(self.ServiceCharge(balance, rate))

                if float(self.ObtainBalance(user)) >= float(balance):
                    A = self.ChangeUser(user=user, menoy=money)
                    B = self.ChangeUser(user=to, menoy=money, mode="+")
                    if A and B:
                        Loggs().Finance("%s 向 %s 支付：￥%f，手续费率：%f，手续费：￥%f，实际到账：￥%f。交易备注：%s" % (user, to, float(balance), float(rate), float(service), float(money), reason))
                        return True
                    else:
                        print("付款操作失败")
                        return False
                else:
                    print("转账失败，您的账户余额不够")
                    return False

            else:
                print("操作失败")
                return False
        else:
            return False

    ''' 处理手续费 
            menoy：交易金额
            rate：费率
    '''
    def ServiceCharge(self, menoy,rate):
        if float(rate) == 0.0:
            return 0
        else:
            return float(menoy) * float(rate)

    ''' 修改用户账户余额 
            user：交易对象
            menoy：金额
            mode：交易方式
    '''
    def ChangeUser(self,user,menoy, mode = "-"):
        users = self.ObtainUsers(user)
        if mode == "-":
            users[user]["balance"] = float(users[user]["balance"]) - float(menoy)
        else:
            users[user]["balance"] = float(users[user]["balance"]) + float(menoy)
        with open(self.__DB_user, "w") as f:
            json.dump(users,f)
            return True

    ''' 获取用户表信息 
            user：用户名称
    '''
    def ObtainUsers(self,user):
        with open(self.__DB_user, "r") as f:
            return json.loads(f.read())

    ''' 用户状态控制 
            user：用户名称
    '''
    def __ControlStatus(self, user):
        users = self.__GetUser(self.__ObtainUser())
        toUser = self.__GetUser(user)
        usersStatus = users["status"]
        userUserstatus = users["userstatus"]
        toUserStatus = toUser["status"]
        toUserUserstatus = toUser["userstatus"]
        if int(usersStatus) != 0:
            print("您的账户被冻结，不能进行该操作！")
            return False
        elif int(userUserstatus) != 0:
            print("您输入的账户有误")
            return False
        elif int(toUserUserstatus) != 0:
            print("您输入的账户有误")
            return False
        elif int(toUserStatus) != 0:
            print("对方的账户被冻结，不能进行该操作！")
            return False
        else:
            return True

    ''' 判断商品状态 
            goods_id：商品ID
            num：数量
    '''
    def __GoodStatus(self, goods_id, num=1):
        read = self.__ReadGoods()[goods_id]
        if read["status"]:
            if read["belongTo"] == self.__ObtainUser():
                print("自己不能购买自己的商品！")
                return False
            else:
                if int(read["goodsType"]) == 1 and int(read["Stock"]) >= int(num):
                    return True
                elif int(read["goodsType"]) == 2:
                    return True
                else:
                    print("您购买的商品库存不够哦！")
                    return False

        else:
            print("Sorry！您购买的商品已下架！")
            return False

    ''' 购买成功后修改商品库存信息 
            goods_id：商品ID
            num：购买数量
    '''
    def __ModifyGoodsInformation(self, goods_id, num=None):
        information = self.__ReadGoods()
        if num == None:
            return True
        else:
            information[goods_id]["Stock"] = int(information[goods_id]["Stock"]) - int(num)
            if self.__WriteGoods(information):
                return True
            else:
                return False

    ''' 制作OrderID 
            user：当前用户
            to：交易对象
    '''
    def __MakeOrderId(self, user, to):
        return Tshash().Jam_hash(user + to + str(time.time())+str(random.randint(1000,9999)))

    ''' 交易成功后，修改订单信息 
            money：金额
            to：交易对象
            ServiceCharge：手续费
            operation：交易类型
            remarks：备注
            rate：手续费率
    '''
    def __ModifyOrderInformation(self, money, to, ActualAccount, ServiceCharge, operation=3,remarks="",rate=0.0):
        money = int(money)
        operation = int(operation)
        information = self.__ReadOrder()
        user = self.__ObtainUser()
        if user:
            OrderId = self.__MakeOrderId(user, to)
            information[OrderId] = {}
            information[OrderId]["user"] = user
            information[OrderId]["operation"] = operation
            information[OrderId]["money"] = money
            information[OrderId]["touser"] = to
            information[OrderId]["status"] = 1
            information[OrderId]["rate"] = float(rate)
            information[OrderId]["ServiceCharge"] = float(ServiceCharge)
            information[OrderId]["ActualAccount"] = float(ActualAccount)
            information[OrderId]["remarks"] = remarks
            information[OrderId]["createdtime"] = time.time()
            information[OrderId]["updatedtime"] = time.time()
            information[OrderId]["deletedtime"] = None
            # {'65d01dc7fa6cb7178972cb5c62be234fa1559494': {'user': 'root', 'operation': 3, 'money': 500, 'touser': 'Alvin', 'status': 1, 'createdtime': 1513351940.6982005, 'updatedtime': 1513351940.6982005, 'deletedtime': None}}
            if self.__WriteOrder(information):
                return True
            else:
                return False
        else:
            return False

    ''' 购买商品
            goods_id：商品名称
            money：商品价格
            num：购买数量
            rate：手续费率
    '''
    def __BeyGoods(self, goods_id, money, num, rate = 0.0001):
        user = self.__ObtainUser()
        if user:
            if self.__ControlStatus(self.__ObtainUser()):
                if self.__GoodStatus(goods_id, num):
                    if self.__ModifyGoodsInformation(goods_id, num):
                        goods = self.__ReadGoods()
                        if self.TransferAccounts(money, goods[goods_id]["belongTo"], rate, "购买商品"):
                            ServiceChange = self.ServiceCharge(money, rate)
                            ActualAccount = float(money) - float(ServiceChange)
                            if self.__ModifyOrderInformation(money, goods[goods_id]["belongTo"], ActualAccount, ServiceChange, 3, "购买"+goods[goods_id]["goodsName"]+"商品" , rate):
                                return True
                            else:
                                return False
                    else:
                        print("Sorry！商品信息操作错误！")
                        return False
                else:
                    return False
            else:
                return False

    ''' 购买商品接口 
        goods_id：商品ID
        num：数量
    '''
    def InterfaceOfBeyGoods(self, goods_id, num):
        if self.__ObtainUser():
            goods = self.__ReadGoods()[goods_id]
            money = goods["goodsParice"]
            if self.__BeyGoods(goods_id, money, num):
                if Cart().DelCartOnce(goods_id):
                    print("交易成功！GoodsName：%s，Number：%s" % (goods["goodsName"],num))
                else:
                    print("交易成功！购物车未修改信息")
                return True
            else:
                return False

    ''' 查询订单信息 '''
    def GetOrder(self, user):
        read = self.__ReadOrder()
        user = self.__ObtainUser()
        information = {}
        information[user] = {}
        for i in read:
            if read[i]["user"] == user:
                information[user] = read[i]
                information[user]["order_id"] = i
        return information




