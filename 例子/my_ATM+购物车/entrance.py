# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/18 0018

from module.user_manage import UserManage


def main():
    while True:
        content = input("What are you going to do([1]Shopping 、[2]ATM(User) or [3]Goods)?").strip()
        while True:
            if str(content) == "1":
                contents = input(
                    "[1]：添加购物车，[2]：结算，[3]：查看购物车信息，[4]：删除购物车商品，[5]：清空购物车，[6]：修改购物车，[7]：获取购物车总金额，[8]：获取购物车某商品总金额，[9]：结算单个商品,[q/Q退出]").strip()
                if contents == "q" or contents == "Q":
                    break
                if contents == "1":
                    break
                else:
                    print("输入错误！请重新输入")
                    break
            elif str(content) == "2":
                contents = input(
                    "[1]：查看余额，[2]：还款，[3]：转账，[4]：修改用户账户余额，[5]：订单查询，[6]：删除用户,[7]:软删除用户，[8]：恢复用户，[9]：冻结用户,[10]：解冻用户，[11]：添加用户,[q/Q退出]").strip()
                if contents == "q" or contents == "Q":
                    break
                if str(contents) == "1":
                    user = UserManage().obtain_username()
                else:
                    print("输入错误！请重新输入")
                    break
            elif str(content) == "3":
                contents = input(
                    "[1]：添加商品，[2]：删除商品，[3]：下架商品，[4]：上架商品，[5]：冻结商品，[6]：解冻商品,[q/Q退出]").strip()
                if contents == "q" or contents == "Q":
                    break
                if str(contents) == "1":
                    pass
                else:
                    print("输入错误！请重新输入")
                    break
            else:
                print("输入错误！请重新输入")
                content = ""
                break


if __name__ == "__main__":
    main()
