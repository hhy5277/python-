# -*- coding:utf-8 -*-
# AUTHER   @ Alvin

import os
import json
import time
from module.Logs import Loggs
from module.Tshash import Tshash

class Cookie(object):
    ''' Cookie操作 '''
    def __init__(self):
        ''' 获取系统类型 '''
        self.__GenreSystem = os.name
        self.__CreateFolder()
        self.__sep = os.path.sep

    ''' 判断需要的文件夹是否存在 '''
    def __DwFolder(self, path):
        if os.path.isdir(path):
            return True
        else:
            return False

    ''' cookieID制作 '''
    def __MakeCookie(self, key):
        return Tshash().Jam_hash("cookie_" + key)

    ''' 创建文件夹 '''
    def __CreateFolder(self):
        if self.__GenreSystem == "nt":
            paths = "C:\\.cookie"
            if not self.__DwFolder(paths):
                try:
                    os.makedirs(paths)
                    return True
                except Exception as e:
                    Loggs().Error(str(e) + "CookiePath创建失败！")
                    return False
            return True
        elif self.__GenreSystem == "posix":
            paths = "/User/cookiess"
            if not self.__DwFolder(paths):
                try:
                    os.makedirs(paths)
                    return True
                except Exception as e:
                    Loggs().Error(str(e) + "CookiePath创建失败！")
                    return False
        else:
            return False

    ''' 获取当前系统Cookie文件夹路径 '''
    def __DwCookiePath(self):
        Wpaths = "C:\\.cookie"
        Mpaths = "/User/cookiess"
        if self.__GenreSystem == "nt" and self.__DwFolder(Wpaths):
            return Wpaths
        elif self.__GenreSystem == "posix" and not self.__DwFolder(Mpaths):
            return Mpaths
        else:
            return False

    ''' 获取当前系统Cookie路径 '''
    def __DwCookiefilePath(self):
        paths = self.__DwCookiePath()
        if paths:
            if self.__GenreSystem == "nt":
                if not os.path.exists(paths + "\cookie.json"):
                    with open(paths + "\cookie.json", "w") as f:
                        pass
                return paths + "\cookie.json"
            else:
                return paths + "/cookie.json"
        else:
            return False

    ''' 判断Cookie是否有效 '''
    def __CookieYrN(self):
        cookie_path = self.__DwCookiefilePath()
        reads = ""
        count = False
        with open(cookie_path, "r") as f:
            reads = json.loads(f.read())
            times = reads["times"]
            Ttime = os.stat(cookie_path).st_mtime
            if int(time.time()) - times > Ttime:
                count = True
            else:
                count = False
        if count:
            with open(cookie_path, "w") as f:
                reads["status"] = False
                json.dump(reads, f)
                return False
        else:
            return True

    ''' 获取Cookie '''
    def __getitem__(self, item):
        cookie_path = self.__DwCookiefilePath()
        count = False
        read = ""
        if cookie_path:
            with open(cookie_path, "r") as f:
                read = f.read()
                if read != "" and json.loads(read) != "":
                    if json.loads(read)["cookie"] == self.__MakeCookie(item):
                        if json.loads(read)["status"] == True:
                            count = True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        if count:
            if self.__CookieYrN():
                return json.loads(read)["sessionid"]
            else:
                return False

    ''' 创建Cookie '''
    def __setitem__(self, key, value):
        cookie_path = self.__DwCookiefilePath()
        cookieId = self.__MakeCookie(key)
        if cookie_path:
            cookie = {"cookie":cookieId, key : value, "times" : 3600, "status":True, "createtime":time.time()}
            with open(cookie_path, "w") as f:
                json.dump(cookie, f)
                return True
        else:
            return False

    ''' 删除Cookie '''
    def __delitem__(self, key):
        cookie_path = self.__DwCookiefilePath()
        if cookie_path:
            with open(cookie_path,"w") as f:
                json.dump("", f)
                return True
        else:
            return False

    ''' 修改Cookie有效期 '''
    def ExpiryTime(self, cookieid, times=3600):
        cookie_path = self.__DwCookiefilePath()
        if cookie_path:
            read = {}
            with open(cookie_path, "r") as f:
                read = json.loads(f.read())

            with open(cookie_path, "w") as f:
                read["times"] = times
                read["status"] = True
                json.dump(read, f)
                return True

    ''' 判断当前系统是否存储登录信息并判断是否有效 '''
    def UserCookieYrN(self):
        paths = self.__DwCookiefilePath()
        if os.path.exists(paths):
            if self.__CookieYrN():
                return True
            else:
                return False
        else:
            return False



# Cookie().UserCookieYrN()
# Cookie()["sessionid"] = "12f95bb180732f456147270c869934adcd16797d"
# print(Cookie()["sessionid"])
# print(Cookie())
# del Cookie()["sads"]
# Cookie().ExpiryTime("sessionid",3600)


