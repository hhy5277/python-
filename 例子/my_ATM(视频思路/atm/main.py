# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/15 0015

# 主要文件 应该包含入口文件所需的函数

from .util import print_red, print_blue, print_green
from .auth import authenticate
from .logger import access_log
from atm import logics

featrues = [
    ("账户信息", logics.view_account_info),
    ("取款", logics.with_draw),
    ("还款", logics.repay)
]


def controller(user_obj):
    while True:
        for index, featrue in enumerate(featrues):  # 循环结束后 feature保留最后一个值在作用域中
            print(index, featrue[0])
        print("输入exit退出")
        choice = input("请选择序号")
        if not choice: continue
        if choice.isdigit():
            choice = int(choice)
            print(featrues[choice][1], "??")
            if choice < len(featrues) and choice >= 0:
                featrues[choice][1](user_obj)
            if choice == "exit":
                exit("bye")


def entrance():
    """
    ATM程序交互入口
    :return:
    """

    user_obj = {  # 用户的内存信息 ,每一次操作内存信息都应该同步到数据文件中
        "is_authenticated": False,
        "data": None
    }

    retry_count = 0  # 用户连续登陆失败次数
    while user_obj["is_authenticated"] is not True:
        account = input("\033[1;34m  账号： \033[0m").strip()
        password = input("\033[1;34m  密码： \033[0m").strip()
        # 需要一个验证账号并返回账号信息的函数 失败返回 None
        auth_data = authenticate(account, password)

        if auth_data:
            user_obj["is_authenticated"] = True
            user_obj["data"] = auth_data
            print_green("-----欢迎登陆-----")

            # 记录日志
            # create_logger("log")
            access_log.info("用户 '%s' 登录成功" % (user_obj["data"]["id"]))
            controller(user_obj)
        else:
            # 没有数据返回说明没有对应的账户信息
            print_red("用户名或密码错误,请重新输入")

        retry_count += 1

        if retry_count == 3:
            msg = "用户名或密码错误到达三次，退出程序"
            print_red(msg)
            break
