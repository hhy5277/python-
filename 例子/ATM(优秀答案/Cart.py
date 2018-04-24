# -*- coding:utf-8 -*-
# AUTHER   @ Alvin
import re
import time
from module.Goods import Goods
from module.Carts import Cart
from module.Order import Order
from module.User import User


def main():
    while True:
        content = input("What are you going to do([1]Shopping 、[2]ATM(优秀答案(User) or [3]Goods)?").strip()
        while True:
            if str(content) == "1":
                contents = input(
                    "[1]：添加购物车，[2]：结算，[3]：查看购物车信息，[4]：删除购物车商品，[5]：清空购物车，[6]：修改购物车，[7]：获取购物车总金额，[8]：获取购物车某商品总金额，[9]：结算单个商品").strip()
                if contents == "q" or contents == "Q":
                    break
                if int(contents) == 1:
                    goods = Goods().GetGoodsInformation()
                    for i in goods:
                        print("商品ID：%s，商品名称：%s" % (i, goods[i]))
                    while True:
                        goods_id = input("请选择需要加入购物车的商品的ID(20171225247617)：").strip()
                        if goods_id == "q" or goods_id == "Q":
                            break
                        num = input("请输入添加数量").strip()
                        if re.search(r'\d+', num) == None:
                            print("数据格式不正确")
                            break
                        else:
                            if Cart().AddCart(goods_id, int(num)):
                                print("添加成功")
                                break
                            else:
                                print("添加失败")
                                break
                elif int(contents) == 2:
                    if contents == "q" or contents == "Q":
                        break
                    cart = Cart().ObtainInstanced().ObtainResult()
                    for i in cart:
                        Order().InterfaceOfBeyGoods(i, cart[i]["goodsNum"])
                        break
                elif int(contents) == 3:
                    if contents == "q" or contents == "Q":
                        break
                    cart = Cart().ObtainInstanced().ObtainResult()
                    for i in cart:
                        print("商品名称：%s，数量：%s，金额：%f" % (
                            cart[i]["goodsName"], cart[i]["goodsNum"], Cart().ObtainOnecMenoy(i)))
                    print("总金额：%f" % (Cart().ObtainAllMenoy()))
                elif int(contents) == 4:
                    if contents == "q" or contents == "Q":
                        break
                    cart = Cart().ObtainInstanced().ObtainResult()
                    for i in cart:
                        print("ID：%s，商品名称：%s" % (i, cart[i]["goodsName"]))
                    goodsId = input("商品ID：").strip()
                    if goodsId == "q" or goodsId == "Q":
                        break
                    if goodsId in cart:
                        if Cart().DelCartOnce(goodsId):
                            print("删除成功！")
                        else:
                            print("删除失败！")
                    else:
                        print("该商品不存在")
                    break
                elif int(contents) == 5:
                    if contents == "q" or contents == "Q":
                        break
                    if Cart().ObtainInstanced().DelCartAll():
                        print("购物车已清空!")
                    else:
                        print("未做操作！")
                    break
                elif int(contents) == 6:
                    if contents == "q" or contents == "Q":
                        break
                    cart = Cart().ObtainInstanced().ObtainResult()
                    for i in cart:
                        print("ID：%s，GoodsName：%s，number：%s" % (i, cart[i]["goodsName"], cart[i]["goodsNum"]))
                    goodsId = input("GoodsID：").strip()
                    num = input("Number：").strip()
                    try:
                        int(num)
                    except Exception as e:
                        print("数量数据不合法")
                        break
                    if goodsId in cart:
                        Cart().ObtainInstanced().ModifyCart(goodsId, num)
                    else:
                        print("购物车不存在该ID商品")
                    break
                elif int(contents) == 7:
                    if contents == "q" or contents == "Q":
                        break
                    AllMenoy = Cart().ObtainInstanced().ObtainAllMenoy()
                    if AllMenoy:
                        print("总金额：%s" % (float(AllMenoy)))
                    else:
                        print("购物车空空如也！！！")
                    break
                elif int(contents) == 8:
                    if contents == "q" or contents == "Q":
                        break
                    cart = Cart().ObtainInstanced().ObtainResult()
                    for i in cart:
                        print("ID：%s，GoodsName：%s，number：%s" % (i, cart[i]["goodsName"], cart[i]["goodsNum"]))
                    goodsId = input("ID:").strip()
                    if goodsId in cart:
                        menoy = Cart().ObtainInstanced().ObtainOnecMenoy(goodsId)
                        if menoy:
                            print("GoodsName：%s，总金额：%s" % (cart[goodsId]["goodsName"], float(menoy)))
                        else:
                            print("操作失败")
                    else:
                        print("):ID不存在")
                elif int(contents) == 9:
                    if contents == "q" or contents == "Q":
                        break
                    cart = Cart().ObtainInstanced().ObtainResult()
                    for i in cart:
                        print("ID: %s，商品名称：%s，数量：%s，金额：%f" % (
                            i, cart[i]["goodsName"], cart[i]["goodsNum"], Cart().ObtainOnecMenoy(i)))
                    goodsId = input("ID:").strip()
                    if goodsId in cart:
                        Order().InterfaceOfBeyGoods(goodsId, cart[goodsId]["goodsNum"])
                    else:
                        print("商品ID：不存在！")
                    break
                else:
                    print("输入错误！请重新输入")
                    break
            elif str(content) == "2":
                contents = input(
                    "[1]：查看余额，[2]：还款，[3]：转账，[4]：修改用户账户余额，[5]：订单查询，[6]：删除用户,[7]:软删除用户，[8]：恢复用户，[9]：冻结用户,[10]：解冻用户，[11]：添加用户").strip()
                if contents == "q" or contents == "Q":
                    break
                if str(contents) == "1":
                    # 余额
                    user = User().ObtainUsername() #返回用户账号
                    if user:
                        print("余额：%s" % (float(Order().ObtainBalance(user))))
                elif str(contents) == "2":
                    user = User().ObtainUsername()
                    if user:
                        menoy = input("menoy：").strip()
                        if re.search("\d+", menoy):
                            Order().Repayment(float(menoy))
                        else:
                            print("您输入的数据不合法")
                elif str(contents) == "3":
                    user = User().ObtainUsername()
                    if user:
                        menoy = input("转账金额：").strip()
                        username = User().GetUserAll()
                        print(username)
                        to = input("转账对象：").strip()
                        if re.search("\d+", menoy):
                            if to in username:
                                if Order().TransferAccounts(menoy, to, reason=str(user + " to " + to), operation=1):
                                    print("操作成功！")
                                else:
                                    print("操作失败")
                            else:
                                print("您输入的用户不存在")
                        else:
                            print("您输入的数据不合法")
                elif str(contents) == "4":
                    user = User().ObtainUsername()
                    if user:
                        if user == "root":
                            menoy = input("操作的金额：").strip()
                            if re.search("\d+", menoy):
                                users = User().GetUserAll()
                                username = input("UserName：").strip()
                                if username in users:
                                    mode = input("操作方式(+ or -)").strip()
                                    if mode == "+" or mode == "-":
                                        User().ChangeUser(username, float(menoy), mode)
                                    else:
                                        print("操作方式不合法")

                            else:
                                print("数据不合法")
                        else:
                            print("无权此操作")
                elif str(contents) == "5":
                    user = User().ObtainUsername()
                    if user:
                        # {'Alvin': {'user': 'Alvin', 'operation': 1, 'money': 200, 'touser': 'root', 'status': 1, 'rate': 0.005, 'ServiceCharge': 0.1, 'ActualAccount': 200.1, 'remarks': '还款', 'createdtime': 1513411904.6930377, 'updatedtime': 1513411904.6930377, 'deletedtime': None}}
                        order = Order().GetOrder(user)
                        print("  订单详情(Start)  ".center(90, "*"))
                        try:
                            print('''
                                                    ID: %s，
                                                    Menoy: %s，
                                                    To: %s，
                                                    Operation(操作方式): %s，
                                                    ActualAccount(实际到账): %s，
                                                    ServiceCharge(手续费): %s，
                                                    rate(手续费率): %s，
                                                    CreatedTime: %s
                                                    ''' % (
                                order[user]["order_id"],
                                float(order[user]["money"]),
                                order[user]["touser"],
                                order[user]["remarks"],
                                float(order[user]["ActualAccount"]),
                                float(order[user]["ServiceCharge"]),
                                float(order[user]["rate"]),
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(order[user]["createdtime"]))
                            ))
                        except Exception as e:
                            print('''
                            一首空空送给你！
                            ''')
                        print("  订单详情(END)  ".center(90, "*"))
                elif str(contents) == "6":
                    user = User().ObtainUsername()
                    if user and user == "root":
                        username = User().GetUserAll()
                        print(username)
                        users = input("用户名称：").strip()
                        if users in username:
                            if User().DelUser(users):
                                print("删除成功")
                            else:
                                print("删除失败！")
                        else:
                            print("输入用户不存在！")
                    else:
                        print("无权操作")
                elif str(contents) == "7":
                    user = User().ObtainUsername()
                    if user and user == "root":
                        username = User().GetUserAll()
                        print(username)
                        users = input("用户名称：").strip()
                        if users in username:
                            if User().ReUser(users):
                                print("删除成功")
                            else:
                                print("删除失败！")
                        else:
                            print("输入用户不存在！")
                    else:
                        print("无权操作")
                elif str(contents) == "8":
                    user = User().ObtainUsername()
                    if user and user == "root":
                        username = User().GetUserAll(userstatus=1)
                        if username:
                            print(username)
                            users = input("用户名称：").strip()
                            if users in username:
                                if User().rReUser(users):
                                    print("恢复成功")
                                else:
                                    print("恢复失败！")
                            else:
                                print("输入用户不存在！")
                        else:
                            print("无用户需要回复")
                    else:
                        print("无权操作")
                elif str(contents) == "9":
                    user = User().ObtainUsername()
                    if user and user == "root":
                        username = User().GetUserAll(status="status", userstatus=0)
                        if username:
                            print(username)
                            users = input("用户名称：").strip()
                            if users in username:
                                if User().FrozenUser(users):
                                    print("冻结成功")
                                else:
                                    print("冻结失败！")
                            else:
                                print("输入用户不存在！")
                        else:
                            print("无用户需要此操作")
                    else:
                        print("无权操作")
                elif str(contents) == "10":
                    user = User().ObtainUsername()
                    if user and user == "root":
                        username = User().GetUserAll(status="status", userstatus=1)
                        if username:
                            print(username)
                            users = input("用户名称：").strip()
                            if users in username:
                                if User().rFrozenUser(users):
                                    print("解冻成功")
                                else:
                                    print("解冻失败！")
                            else:
                                print("输入用户不存在！")
                        else:
                            print("无用户需要此操作")
                    else:
                        print("无权操作")
                elif str(contents) == "11":
                    user = User().ObtainUsername()
                    if user:
                        if user == "root":
                            username = input("Username:").strip()
                            password = input("Password:").strip()
                            if re.search("\w+", username) and re.search("\w+", password):
                                if User().AddUser(username, password):
                                    print("添加成功")
                                else:
                                    print("添加失败")
                            else:
                                print("用户名或密码不合法")
                        else:
                            print("无权操作")
            elif str(content) == "3":
                contents = input(
                    "[1]：添加商品，[2]：删除商品，[3]：下架商品，[4]：上架商品，[5]：冻结商品，[6]：解冻商品").strip()
                if contents == "q" or contents == "Q":
                    break
                if str(contents) == "1":
                    if Goods().AddGoods():
                        print("添加成功")
                    else:
                        print("添加失败")
                elif str(contents) == "2":
                    goods = Goods().GetGoodsUserInformation()
                    if goods:
                        for i in goods:
                            print("ID：%s，GoodsName：%s" % (i, goods[i]["goodsName"]))
                    else:
                        print("没有您可操作性的商品")
                        break
                    goodsId = input("商品ID：").strip()
                    if goodsId == "q" or goodsId == "Q":
                        break
                    if int(goodsId) in goods:
                        if Goods().DelGoods(goodsId):
                            print("删除成功")
                        else:
                            print("删除失败")

                    else:
                        print("您输入的ID不存在")
                    break
                    # Goods().DelGoods()
                elif str(contents) == "3":
                    goods = Goods().GetGoodsUserInformation()
                    if goods:
                        count = False
                        for i in goods:
                            if goods[i]["status"] and goods[i]["goodsStatus"]:
                                count = True
                                print("ID：%s，GoodsName：%s" % (i, goods[i]["goodsName"]))
                        if not count:
                            print("没有您可下架的商品")
                            break
                    else:
                        print("没有您可下架的商品")
                        break
                    goodsId = input("商品ID：").strip()
                    if goodsId == "q" or goodsId == "Q":
                        break
                    if int(goodsId) in goods:
                        if Goods().GoodsoffShelves(goodsId):
                            print("下架成功")
                        else:
                            print("下架失败")
                    else:
                        print("您输入的ID不存在")
                    break
                elif str(contents) == "4":
                    goods = Goods().GetGoodsUserInformation()
                    if goods:
                        count = False
                        for i in goods:
                            if not goods[i]["goodsStatus"]:
                                count = True
                                print("ID：%s，GoodsName：%s" % (i, goods[i]["goodsName"]))
                        if not count:
                            print("没有您可上架的商品")
                            break
                    else:
                        print("没有您可上架的商品")
                        break
                    goodsId = input("商品ID：").strip()
                    if goodsId == "q" or goodsId == "Q":
                        break
                    if int(goodsId) in goods:
                        if Goods().GoodsOnShelves(goodsId):
                            print("上架成功")
                        else:
                            print("上架失败")
                    else:
                        print("您输入的ID不存在")
                    break
                elif str(contents) == "5":
                    goods = Goods().GetGoodsUserInformation()
                    if goods:
                        count = False
                        for i in goods:
                            if not goods[i]["goodsStatus"]:
                                count = True
                                print("ID：%s，GoodsName：%s" % (i, goods[i]["goodsName"]))
                        if not count:
                            print("没有您可冻结的商品")
                            break
                    else:
                        print("没有您可冻结的商品")
                        break
                    goodsId = input("商品ID：").strip()
                    if goodsId == "q" or goodsId == "Q":
                        break
                    if int(goodsId) in goods:
                        if Goods().FrozenGoods(goodsId):
                            print("冻结成功")
                        else:
                            print("冻结失败")
                    else:
                        print("您输入的ID不存在")
                    break
                elif str(contents) == "6":
                    goods = Goods().GetGoodsUserInformation()
                    if goods:
                        count = False
                        for i in goods:
                            if not goods[i]["status"]:
                                count = True
                                print("ID：%s，GoodsName：%s" % (i, goods[i]["goodsName"]))
                        if not count:
                            print("没有您可解冻的商品")
                            break
                    else:
                        print("没有您可解冻的商品")
                        break
                    goodsId = input("商品ID：").strip()
                    if goodsId == "q" or goodsId == "Q":
                        break
                    if int(goodsId) in goods:
                        if Goods().rFrozenGoods(goodsId):
                            print("解冻成功")
                        else:
                            print("解冻失败")
                    else:
                        print("您输入的ID不存在")
                    break
                else:
                    print("输入错误！请重新输入")
                    break
            else:
                print("输入错误！请重新输入")
                content = ""
                break


if __name__ == "__main__":
    main()
