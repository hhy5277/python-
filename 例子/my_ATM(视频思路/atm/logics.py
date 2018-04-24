# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/16 0016

from .logger import transaction_log, access_log
from .util import print_red, print_green
from .transaction import make_transaction


def view_account_info(account_data, *args, **kwargs):
    transaction_log.info("用户 '%s' 查看账户信息" % (account_data["data"]["id"]))

    print("ACCOUNT INFO".center(50, "-"))
    for k, v in account_data["data"].items():
        if k not in ("password",):
            print("%15s：%s" % (k, v))
    print("END".center(50, "-"))


def with_draw(account_data, *args, **kwargs):
    access_log.info("进入取款")
    current_balance = """  ---   BALANCE  INFO  ---
         Credit :%s
        Balance :%s""" % (account_data["data"]["credit"], account_data["data"]["balance"])
    print(current_balance)
    while True:
        withdraw_mount = input('\033[1;32m  输入你的取款金额(b ：退出) \033[0m').strip()
        if len(withdraw_mount) > 0 and withdraw_mount.isdigit():
            withdraw_mount = int(withdraw_mount)
            if (account_data["data"]["balance"] / 2 >= withdraw_mount):
                transaction_result = make_transaction(account_data, "with_draw", withdraw_mount)
                if transaction_result["status"] == 0:
                    transaction_log.info("用户%s成功取出%s" % (account_data["data"]["id"], withdraw_mount))
                    print_green("最新余额%s" % (account_data["data"]["balance"]))
                else:
                    print(transaction_result)
            else:
                print_red("可取余额不足，可提现%s" % (int(account_data["data"]["balance"]) / 2))

        if withdraw_mount == "b":
            access_log.info("退出取款")
            break


def repay(account_data, *args, **kwargs):
    access_log.info("进入还款")
    current_balance = """  ---   BALANCE  INFO  ---
             Credit :%s
            Balance :%s""" % (account_data["data"]["credit"], account_data["data"]["balance"])
    print(current_balance)
    pay_mount = input('\033[1;32m  输入你的还款金额(b ：退出) \033[0m').strip()
    if len(pay_mount) > 0 and pay_mount.isdigit():
        pay_mount = int(pay_mount)
        transaction_result = make_transaction(account_data, "repay", pay_mount)

        if transaction_result["status"] == 0:
            print("还款成功")
        else:
            print("还款失败")
