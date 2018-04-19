# -*- coding:utf-8 -*-
# AUTHER   @ Alvin
import os
import json
import time
import random
from module.User import User
import re
class Goods(object):

    def __init__(self):
        self.__sep = os.path.sep
        self.__Goods = os.path.abspath("DB/DB_table/goods.json")

    ''' 添加商品 '''
    def AddGoods(self):
        if self.getUserJurisdictionYorN(Jurisdiction=1):
            # {'goodsName': '美女', 'goodsParice': '123', 'belongTo': '陈阳', 'status': 'y', 'goodsType': '1', 'Stock': '20'}
            information = self.__GoodsInformation(gName=True,gParice=True,gstatus=True,gType=True)
            goodsID = int(time.strftime("%Y%m%d%H%M%S", time.localtime())) + random.randint(10000000, 99999999)
            information["goodsId"] = goodsID
            information["belongTo"] = self.GetUser()
            information["goodsStatus"] = True
            read = ""
            with open(self.__Goods, "r") as f:
                fread = f.read()
                if fread == "":
                    read = {}
                else:
                    read = json.loads(fread)
            read[goodsID] = information
            with open(self.__Goods, "w") as f:
                json.dump(read, f)
                return True
        else:
            return False

    ''' 商品信息录入 '''
    def __GoodsInformation(self, gName=False, gParice=False,gbelongTo=False,gstatus=False,gType=False):
        information = {}
        count = "您添加的商品如下："
        if gName:
            while True:
                goodsName = input("商品名称：").strip()
                if self.InterfaceInput(goodsName, "\W+"):
                    information["goodsName"] = goodsName
                    count += "商品名称：" + goodsName + "，"
                    break
                else:
                    print("非法商品名称！")
        if gParice:
            while True:
                goodsParice = input("商品价格：").strip()
                if self.InterfaceInput(goodsParice, "\D+"):
                    information["goodsParice"] = goodsParice
                    count += "商品价格：" + goodsParice + "，"
                    break
                else:
                    print("非法商品价格！")
        if gbelongTo:
            while True:
                belongTo = input("商家：").strip()
                if self.InterfaceInput(belongTo, "\W+"):
                    information["belongTo"] = belongTo
                    count += "商家：" + belongTo + "，"
                    break
                else:
                    print("非法商品名称！")
        if gstatus:
            while True:
                status = input("是否上架(Y or N)：").strip()
                if not self.InterfaceInput(status, "Y|N|y|n"):
                    if status == "Y" or status == "y":
                        information["status"] = True
                        count += "上架，"
                        break
                    else:
                        information["status"] = False
                        count += "下架，"
                        break
                else:
                    print("非法商品上架信息(Y|N|y|n)！")

        if gType:
            while True:
                goodsType = input("商品类型(1:实体商品 or 2:虚拟商品)：").strip()
                if not self.InterfaceInput(goodsType, "\d+"):
                    if int(goodsType) == 1 or int(goodsType) == 2:
                        information["goodsType"] = goodsType
                        if int(goodsType)==1:
                            count += "实体商品，"
                        else:
                            count += "虚拟商品，"
                        break
                    else:
                        print("非法商品类型！(1 or 2)")
                else:
                    print("非法商品类型！(1 or 2)")
            while True:
                if int(goodsType) == 1:
                    Stock = input("库存：").strip()
                    if self.InterfaceInput(Stock, "\D+"):
                        information["Stock"] = Stock

                        break
                    else:
                        print("非法商品库存！")
                else:
                    information["Stock"] = False
                    break
                count += "库存为：" + Stock

        print(count)
        return information

    ''' 正则输入接口 '''
    def InterfaceInput(self, content, res):
        if not re.search(res, content):
            return True
        else:
            return False

    ''' 删除商品 '''
    def DelGoods(self, goods_id):
        count = False
        if self.__MakeGoodsBelongUser(goods_id):
            count = True
        else:
            if self.__Goods == "root":
                count = True
        if count:
            read = self.__ReadAttributesGoods()
            del read[goods_id]
            with open(self.__Goods, "w") as f:
                json.dump(read, f)
                return True
        else:
            print("无权操作！")
            return False

    ''' 下架商品 '''
    def GoodsoffShelves(self, goods_id):
        information = {"goodsStatus": False}
        if self.__GoodsStatus(goods_id, information):
            return True
        else:
            return False

    ''' 上架商品 '''
    def GoodsOnShelves(self, goods_id):
        information = {"goodsStatus": True}
        if self.__GoodsStatus(goods_id, information):
            return True
        else:
            return False

    ''' 冻结商品 '''
    def FrozenGoods(self, goods_id):
        if self.getUserJurisdictionYorN(0):
            information = {"status": False}
            if self.__GoodsStatus(goods_id, information):
                return True
            else:
                return False
        else:
            print("无权此操作")
            return False

    ''' 解冻商品 '''
    def rFrozenGoods(self, goods_id):
        if self.getUserJurisdictionYorN(0):
            information = {"status": True}
            if self.__GoodsStatus(goods_id, information):
                return True
            else:
                return False
        else:
            print("无权此操作")
            return False

    ''' 商品状态操作 '''
    def __GoodsStatus(self,goods_id, information):
        count = False
        if self.__MakeGoodsBelongUser(goods_id):
            count = True
        else:
            if self.getUserJurisdiction():
                count = True
        if count:
            if self.__ModifyAttributesGoods(goods_id,information):
                return True
            else:
                return False
        else:
            return False

    ''' 商品属性操作 '''
    def __ModifyAttributesGoods(self, goods_id, informition):
        read = self.__ReadAttributesGoods()
        goodsAttrbutes = read[goods_id]
        for i in informition:
            goodsAttrbutes[i] = informition[i]
        with open(self.__Goods, "w") as f:
            json.dump(read, f)
            return True

    ''' 读取商品属性 '''
    def __ReadAttributesGoods(self):
        with open(self.__Goods, "r") as f:
            return json.loads(f.read())

    ''' 获取当前用户信息 '''
    def GetUser(self):
        return User().ObtainUsername()

    ''' 获取当前用户是否有权限 '''
    def getUserJurisdictionYorN(self,Jurisdiction=1):
        return User().JurisdictionYroN(Jurisdiction)

    ''' 获取当前用户是否是超级用户 '''
    def getUserJurisdiction(self):
        Jurisdiction = User().AccesstoJurisdictionUser(self.GetUser())
        if Jurisdiction == False:
            return False
        elif Jurisdiction == "0":
            return True

    ''' 判断当前操作商品是否属于您当前用户 '''
    def __MakeGoodsBelongUser(self, goods_id):
        read = self.__ReadAttributesGoods()
        if read[goods_id]["belongTo"] == self.GetUser():
            return True
        else:
            return False

    ''' 返回所有商品基本信息 '''
    def GetGoodsInformation(self):
        goods = self.__ReadAttributesGoods()
        information = {}

        for i in goods.values():
            information[i["goodsId"]] = {}
            information[i["goodsId"]]["goodsName"] = i["goodsName"]
            information[i["goodsId"]]["belongTo"] = i["belongTo"]
        return information

    ''' 返回当前用户的信息 '''
    def GetGoodsUserInformation(self):
        goods = self.__ReadAttributesGoods()
        information = {}
        user = self.GetUser()
        for i in goods.values():
            if i["belongTo"] == user:
                information[i["goodsId"]] = {}
                information[i["goodsId"]]["goodsName"] = i["goodsName"]
                information[i["goodsId"]]["status"] = i["status"]
                information[i["goodsId"]]["goodsStatus"] = i["goodsStatus"]
        return information

# print(goods.GetGoodsInformation())
# print(Goods().MakeGoodsBelongUser("20171292722236"))


# print(Goods().GoodsOnShelves("20171292722236"))


