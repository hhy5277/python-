# -*- coding:utf-8 -*-
# AUTHER   @ Alvin

import os
import time
import hashlib
import json
from module.Cookies import Cookie

class Session(object):
    ''' session '''
    def __init__(self):
        self.__sessionPath = os.path.abspath("DB/DB_session")
        self.__sessionIDPath = os.path.abspath("DB/DB_table")
        self.__sep = os.path.sep

    '''制作session的ID'''
    def __createSession(self):
        create_session_id = "%s" % (time.time())
        hash = hashlib.sha1()
        hash.update(bytes(create_session_id , encoding="utf-8"))
        return hash.hexdigest()

    ''' 获取session值 '''
    def __getitem__(self, item):
        username = ""
        with open(self.__sessionIDPath + self.__sep +"sessionId.json", "r") as f:
            read = f.read()
            if read != "":
                session_id = json.loads(read)
                if item in session_id:
                    username = session_id[item]
                else:
                    return False
            else:
                return False
        count = False
        try:
            with open(self.__sessionPath + self.__sep + "session_" + item + ".json", "r") as f:
                jsonMake = json.loads(f.read())
                jsonMakes = jsonMake[username]
                expiryTime = jsonMakes["expiryTime"]
                if jsonMakes["expiry"]:
                    Times = time.time() - int(expiryTime)
                    mTimes = os.stat(self.__sessionPath + self.__sep + "session_" + item + ".json").st_mtime
                    if int(Times) > int(mTimes):
                        count = True
                    else:
                        return jsonMakes["user"]
                else:
                    return False
        except Exception as e:
            del Cookie()["sessionid"]
        if count:
            with open(self.__sessionPath + "\\\\session_" + item + ".json", "w") as f:
                jsonMakes["expiry"] = False
                jsonMake[username] = jsonMakes
                json.dump(jsonMake, f)
                return False

    ''' 设置session值 '''
    def __setitem__(self, username, fmm):
        session_ID = self.__createSession()
        Session_data = {}
        Session_data[username] = {"sessionid": session_ID,"user":username,"expiryTime": 3360, "expiry": True, "createTime": time.time()}
        with open(self.__sessionPath + self.__sep +"session_" + session_ID + ".json", "w") as f:
            json.dump(Session_data,f)
        read = ""
        with open(self.__sessionIDPath + self.__sep + "sessionId.json","r") as f:
            read = f.read()
        with open(self.__sessionIDPath +  self.__sep + "sessionId.json", "w") as f:
            if read is "":
                jsonData = {}
            else:
                jsonData = json.loads(read)
            jsonData[session_ID] = username
            Cookie()["sessionid"] = session_ID
            json.dump(jsonData, f)
            return True

    ''' 删除session '''
    def __delitem__(self, user):
        with open(self.__sessionIDPath +  self.__sep + "sessionId.json", "r") as f:
            reads = f.read()
            sessionIds = json.loads(reads)
            if user in sessionIds:
                sessionIds = sessionIds[user]
            else:
                return False
        read = ""
        with open(self.__sessionPath +  self.__sep + "session_" + sessionIds + ".json", "r") as f:
            read = f.read()
        with open(self.__sessionPath +  self.__sep + "session_" + sessionIds + ".json", "w") as f:
            ss = json.loads(read)
            ss[sessionIds]["expiry"] = False
            json.dump(ss, f)
            return True

    ''' 修改过期时间  '''
    def ExpiryTime(self,user,times=3600):
        with open(self.__sessionIDPath +  self.__sep + "sessionId.json", "r") as f:
            reads = f.read()
            sessionIds = json.loads(reads)
            if user in sessionIds:
                sessionIds = sessionIds[user]
            else:
                return False
        read = ""
        with open(self.__sessionPath +  self.__sep + "session_" + sessionIds + ".json", "r") as f:
            read = f.read()
        with open(self.__sessionPath +  self.__sep + "session_" + sessionIds + ".json", "w") as f:
            ss = json.loads(read)
            ss[sessionIds]["expiryTime"] = times
            ss[sessionIds]["expiry"] = True
            json.dump(ss, f)
            return True


# print(Session()["c42e96dcf20f64bf32331669f0f58a64b36867a2"])