# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/17 0017

from conf import setting
from .util import print_red
from .db_handler import save_db


def make_transaction(user_obj, trans_type, amount, **kwargs):
    amount = float(amount)
    if trans_type in setting.TRANSACTION_TYPE:
        interest = amount * setting.TRANSACTION_TYPE[trans_type]["interest"]
        old_balance = user_obj["data"]["balance"]
        if setting.TRANSACTION_TYPE[trans_type]["action"] == "plus":
            new_balance = old_balance + amount - interest
        elif setting.TRANSACTION_TYPE[trans_type]["action"] == "minus":
            new_balance = old_balance - amount - interest
            if new_balance < 0:
                print_red("余额不足，最多可取%s" % (int(old_balance / 2)))
                return {"status": -1, "error": "余额不足，交易失败"}

        user_obj["data"]["balance"] = new_balance
        save_result = save_db(user_obj["data"])
        if save_result["status"] == 0:
            return {"status": 0, "msg": "存取账户信息成功"}
        else:
            return {"status": -1, "msg": "存取账户信息失败"}
