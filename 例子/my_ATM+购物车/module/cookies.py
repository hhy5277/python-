# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/19 0019
import os,json,time
from .handle_hash import Handlehash

'''
cookie 数据结构
    {
    "cookie": "5faa7929070a00ea62cb2e845bd5b4fd2c04bbc5", 
    "sessionid": "6ac7d6337143a3932d9de190044ecd2691d3b4f4", 
    "times": 3600, "status": true,
     "createtime": 1524138589.4231675
     }
'''
class Cookie:
    def __init__(self):
        self.__systemType = os.name
        self.__create_dir()

    ''' 判断需要的文件夹是否存在 '''

    def __dir_is_exist(self, path):
        if os.path.isdir(path):
            return True
        else:
            return False

    '''创建文件夹'''

    def __create_dir(self):
        if self.__systemType == "nt":
            paths = "C:\\.cookie"
            print(self.__dir_is_exist(paths))
            if not self.__dir_is_exist(paths):
                try:
                    os.makedirs(paths)
                    return True
                except Exception as e:
                    print(e)
                    return False
            return True
        elif self.__systemType == "posix":
            paths = "/User/cookiess"
            if not self.__dir_is_exist(paths):
                try:
                    os.makedirs(paths)
                    return True
                except Exception as e:
                    # Loggs().Error(str(e) + "CookiePath创建失败！")
                    print(e)
                    return False
        else:
            return False

    ''' 获取当前系统Cookie文件夹路径 '''

    def __getCookieDirPath(self):
        Wpaths = "C:\\.cookie"
        Mpaths = "/User/cookiess"
        if self.__systemType == "nt" and self.__dir_is_exist(Wpaths):
            return Wpaths
        elif self.__systemType == "posix" and not self.__dir_is_exist(Mpaths):
            return Mpaths
        else:
            return False

    ''' 获取当前系统Cookie文件路径 '''

    def __getCookiefilePath(self):
        paths = self.__getCookieDirPath()
        cookie_paths=os.path.join(paths,"cookie.json")
        if os.path.isfile(cookie_paths):
             return cookie_paths
        else:
            return False

    def __MakeCookie(self,key):
        return Handlehash().encode_hash("cookie_" + key)

    ''' 判断Cookie是否有效 '''
    def __cookieIsUtilize(self):
        cookie_path = self.__getCookiefilePath()
        reads = ""
        count = False
        with open(cookie_path, "r") as f:
            reads = json.loads(f.read())
            times = reads["times"]
            Ttime = os.stat(cookie_path).st_mtime # 最后一次修改时间
            if int(time.time()) - times > Ttime:
                count = True
            else:
                count = False
        print(count, "count")
        if count:
            with open(cookie_path, "w") as f:
                reads["status"] = False
                json.dump(reads, f)
                return False
        else:
            return True

    '''获取cookie'''
    def __getitem__(self, item):
        """
        :param item: "sessionid" 字符串
        :return:
        """
        count=False

        cookie_path=self.__getCookiefilePath()
        if cookie_path:
            with open(cookie_path) as f:
                read =f.read()
                result =json.loads(read)
                if read !="" and result != "":
                    if result["cookie"] == self.__MakeCookie(item):
                        if result["status"]:
                            count = True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        else:
            return False

        if count:
            if self.__cookieIsUtilize():
                return json.loads(read)["sessionid"]
            else:
                return False
