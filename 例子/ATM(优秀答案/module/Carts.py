# -*- coding:utf-8 -*-
# AUTHER   @ Alvin
import os
import json
from module.User import User
# from User import User
import time
class Cart(object):

    def __init__(self):
        self.__information = {}
        self.__DB_SEP = os.path.sep
        self.__DB_Cart = os.path.abspath("DB/DB_table/cart.json")
        self.__Goods = os.path.abspath("DB/DB_table/goods.json")
        self.__GetUserCart()

    ''' 存储当前对象 '''
    __instanced = None

    ''' 添加购物车 '''
    def AddCart(self, goods_id, num=1):
        user = self.__ObtainUser()
        if user:
            goods = self.GetGoodsInformation(goods_id)
            if goods:
                information = {}
                information["goodsName"] = goods["goodsName"]
                information["goodsId"] = goods["goodsId"]
                information["goodsNum"] = int(num)
                information["goodsParice"] = goods["goodsParice"]
                information["createTime"] = time.time()
                cart = self.__GetCartAll()
                if cart == "":
                    carts={}
                else:
                    carts = json.loads(cart)
                if user in carts:
                    pass
                else:
                    carts[user] = {}
                carts[user][goods_id] = information
                write = self.__WriteCart(carts)
                if write:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    ''' 获取当前商品信息 '''
    def GetGoodsInformation(self, goods_id):
        user = self.__ObtainUser()
        if user:
            goods = self.__GetGoodsAll()
            if goods_id in goods:
                return goods[goods_id]
            else:
                print("当前商品不存在")
                return False
            # goods[goods_id]   {'goodsName': '电视', 'goodsParice': '2000', 'status': True, 'goodsType': '1', 'Stock': '200', 'goodsId': 20171225247617, 'belongTo': 'root', 'goodsStatus': True}
        else:
            return False

    ''' 获取所以商品信息 '''
    def __GetGoodsAll(self):
        with open(self.__Goods, "r") as f:
            return json.loads(f.read())

    ''' 返回购物车所有的信息 '''
    def __GetCartAll(self):
        with open(self.__DB_Cart, "r") as f:
            return f.read()

    ''' 清空购物车 '''
    def DelCartAll(self):
        user = self.__ObtainUser()
        if user:
            cart = json.loads(self.__GetCartAll())
            if user in cart:
                YorN = input("此操作购物车无法找回，是否清空购物车(Y or N)")
                if YorN == "Y" or YorN == "y":
                    del cart[user]
                    if self.__WriteCart(cart):
                        return True
                    else:
                        return False
                else:
                    print("操作成功，购物车信息未清空")
                    return False
            else:
                return False
        else:
            return False

    ''' 删除一个商品 '''
    def DelCartOnce(self, goods_id):
        user = self.__ObtainUser()
        if user:
            cart = json.loads(self.__GetCartAll())
            if str(goods_id) in cart[user]:
                del cart[user][str(goods_id)]
            if self.__WriteCart(cart):
                return True
            else:
                return False
        else:
            return False

    ''' 修改购物车商品信息 '''
    def ModifyCart(self, goods_id, num=1):
        cart = json.loads(self.__GetCartAll())
        user = self.__ObtainUser()
        if user in cart:
            if str(goods_id) in cart[user]:
                cart[user][goods_id]["goodsNum"] = num
                if self.__WriteCart(cart):
                    print(":修改成功")
                    return True
                else:
                    print("修改失败")
                    return False
            else:
                print("您的购物车没有此商品")
                return False
        else:
            print("您的购物车是空空的, 赶快去添加吧！")
            return False

    ''' 写入购物车 '''
    def __WriteCart(self, cart):
        with open(self.__DB_Cart, "w") as f:
            json.dump(cart, f)
            return True

    ''' 获取当前用户信息 '''
    def __ObtainUser(self):
        user = User().ObtainUsername()
        if user:
            return user
        else:
            return False

    ''' 返回当前用户购物车信息 '''
    def ObtainResult(self):
        return self.__information

    ''' 获取当前用户的购物车信息 '''
    def __GetUserCart(self):
        user = self.__ObtainUser()
        if user:
            cart = json.loads(self.__GetCartAll())
            if cart == "":
                self.__information = ""
                print("暂无购物车信息")
            else:
                if user in cart:
                    self.__information = cart[user]
                else:
                    self.__information = {}
        else:
            return False

    ''' 获取当前用户单个商品的金额 '''
    def ObtainOnecMenoy(self, goods_id):
        goods_id = str(goods_id)
        user = self.__ObtainUser()
        if user:
            cart = json.loads(self.__GetCartAll())
            # print(cart[user])
            if user in cart:
                if goods_id in cart[user]:
                    num = int(cart[user][goods_id]["goodsNum"])
                    price = int(cart[user][goods_id]["goodsParice"])
                    return num * price
                else:
                    return False
            else:
                return False
        else:
            return False

    ''' 获取当前用户所有商品的金额 '''
    def ObtainAllMenoy(self):
        user = self.__ObtainUser()
        if user:
            cart = json.loads(self.__GetCartAll())
            if user in cart:
                number = 0
                for i in  cart[user]:
                    number += int(cart[user][i]["goodsNum"]) * int(cart[user][i]["goodsParice"])
                return number
            else:
                return False
        else:
            return False

    ''' 获取Cart对象 '''
    @staticmethod
    def ObtainInstanced():
        if Cart.__instanced:
            return Cart.__instanced
        else:
            Cart.__instanced = Cart()
            return Cart.__instanced

# cart = Cart()
# Cart.ObtainInstanced().AddCart("20171225247617", num=2)
# print(Cart.ObtainInstanced().ObtainAllMenoy())
# print(Cart.ObtainInstanced().ObtainAllMenoy())
# print(Cart().ObtainInstanced().__information)