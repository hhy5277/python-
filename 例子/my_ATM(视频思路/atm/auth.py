# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/15 0015

from .util import print_red
from .db_handler import load_account_data


def authenticate(account, password):
    """
     通过账户去获取账户数据
     没有数据、有数据密码不对返回False,否则返回数据
    account_data:  {
                    "status":0    #0成功 -1失败
                    "data"：{}    #用户数据
                  }
    """
    account_data = load_account_data(account)
    if account_data["status"] == 0:  # 如果有数据返回
        account_data = account_data["data"]
        if password == account_data['password']:  # 密码正确则返回用户数据
            return account_data
        else:  # 密码不正确返回None
            return None
    else:  # 如果没有数据返回
        # print_red("没有数据返回")
        return None
