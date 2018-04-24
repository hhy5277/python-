# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/15 0015
# 存取文件信息


# Json   模块提供了四个方法： dumps、dump、loads、load
# load() 第一个参数open的文件对象
# json.dump(obj, fp, *,indent=None)
import json, os
from conf import setting



def load_account_data(account):
    """
    :param account:
    :return: eg：{
        "status":0    #0成功 -1失败
        "data"：{}    #用户数据
    }
    """
    count_file = os.path.join(setting.DB_PATH, "%s.json" % (account))
    # 判断count_file isFile
    if os.path.isfile(count_file):
        with open(count_file) as f:
            data = json.load(f)
            return {
                "status": 0,
                "data": data
            }

    else:
        return {
            "status": -1,
            "data": None
        }


def save_db(account_data):
    account_file=os.path.join(setting.DB_PATH,"%s.json"%(account_data["id"]))
    if os.path.isfile(account_file):
        # f=open("%s.new"%(account_file),"w")
        # data=json.dump(account_data,f)
        with open("%s.new"%(account_file),"w") as f:
            json.dump(account_data, f)

        os.remove(account_file)
        os.rename("%s.new"%(account_file),account_file)

        return{"status":0,"msg":"成功"}
    else:
        return {"status":-1,"error":"账户文件不存在"}