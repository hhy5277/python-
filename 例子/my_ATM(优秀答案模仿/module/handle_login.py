import json, os
from .session import Session
from .handle_hash import Handlehash

class Login:
    def __init__(self):

        self.__DB_path = os.path.abspath("DB")

    ''' 登录 登录过程只负责 验证账户/密码
        验证成功后 更新session
        失败则返回False
    '''

    def __login(self, username, password):
        """

        :param username:
        :param password:
        :return: 登陆成功之后返回True
        """
        with open(os.path.join(self.__DB_path, "DB_table", "user.json"), "r") as f:
            userDict = json.load(f)

            if username in userDict:
                if userDict[username]["password"] == password:
                    # 没登录一次记录一个新的 session
                    #会记录在两个地方 DB_session 和DB_table.user.json
                    Session()[username] = username  # 记录session
                    print("session 记录完成")
                    return True

                else:
                    print("密码不正确")
                    return False

            else:
                print("用户不存在")
                return False

    def user_login(self):
        username = input("用户名：").strip()
        password = input("密码：").strip()
        encodePassword=Handlehash().encode_hash_sha1(password)
        return self.__login(username,encodePassword)   # password应该加密
