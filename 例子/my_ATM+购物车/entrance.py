# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/18 0018

import re
from module.user_manage import UserManage
from module.handle_order import Order


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
                    username = UserManage().obtain_username()
                    if username:
                        print("余额为："+str(Order().ObtainBalance(username)))

                if str(contents) == "2":
                    user = UserManage().obtain_username()
                    if user:
                        menoy = input("menoy：").strip()
                        if re.search("^\d+$", menoy):
                            # Order().Repayment(float(menoy))
                            print(menoy)
                        else:
                            print("您输入的数据不合法")
                else:
                    print("输入错误！请重新输入")
                    break
            else:
                print("输入错误！请重新输入")
                content = ""
                break


if __name__ == "__main__":
    main()
