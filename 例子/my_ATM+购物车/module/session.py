import hashlib,time,os,json
from .cookies import Cookie

class Session:
    def __init__(self):
        self.__DB_session = os.path.abspath("DB/DB_session")
        self.__DB_table = os.path.abspath("DB/DB_table")

    '''制作session的ID'''
    def __createSessionVal(self):
        create_session_id = "%s" % (time.time())
        hash = hashlib.sha1()
        hash.update(bytes(create_session_id, encoding="utf-8"))
        return hash.hexdigest()

    '''设置session #会记录在两个地方 DB_session 和DB_table.user.json'''
    def __setitem__(self, username, value):
        session_value =self.__createSessionVal()  #当前时间戳的sha1加密
        Session_data = {}
        Session_data[username] = {"sessionid": session_value,
                                  "user":username,
                                  "expiryTime": 3360,
                                  "expiry": True,
                                  "createTime": time.time()}


        #写入 DB_session 文件数据  记录 当前username 的对应数据

        with open(os.path.join(self.__DB_session,"session_" + session_value+".json"), "w") as f:
            json.dump(Session_data,f)

        #再写入 DB_table的userjson 记录历史 session_value对应的username
        #注意：该文件记录  session_value 和 username 的对应关系
        with open(os.path.join(self.__DB_table,"sessionid.json"),"r") as f_read:
            user_json_data = json.load(f_read)
            user_json_data[session_value] = username

            # 再创建对应的cookie数据
            Cookie()["sessionid"] = session_value


            # 写入修改后的数据
            with open(os.path.join(self.__DB_table, "sessionid.json"), "w") as f_write:
                json.dump(user_json_data,f_write)

        return True

    '''获取sessionid的值'''
    def __getitem__(self, sessionid):
        # 逻辑  通过sessionid在user.json中获取对应的username
        # 再用username 再DB_session中判断是否过去，未过期则返回该用户所有数据
        '''

        :param sessionid: cookie中sessionid的值
        :return:返回username 账号
        '''
        username = ''
        userjson =os.path.join(self.__DB_table,"sessionId.json")
        if not os.path.isfile(userjson):
            return False
        with open(userjson,"r") as f:
            session_id = json.load(f)
            if session_id:
                if sessionid in session_id:
                    #用sessionid.json中的name 获取DB_session中的数据
                    username = session_id[sessionid]
                else:
                    return False
            else:
                return False

        try:
            with open(os.path.join(self.__DB_session,"session_"+sessionid+".json"),"r") as f:
                session_data=json.load(f)[username]
                #判断是否过期
                if session_data["expiry"]: #没过期
                    if time.time()-session_data["expiryTime"]>session_data["createTime"]:#过期了
                        with open(os.path.join(self.__DB_session, "session_" + sessionid + ".json"),"w") as f1:
                            session_data["expiry"] =False
                            new_session_data={ username:session_data }
                            json.dump(new_session_data,f1)
                    else:
                        return session_data["user"]

                else:#过期
                    return False

        except Exception as e:
            pass
            #删除cookie




