import json, os


class Login:
    def __init__(self):

        self.__DB_path = os.path.abspath("DB")
        # print(self.__DB_path, "__DB_path")
        # print(os.path.join(self.__DB_path, "DB_table", "user.json"), "???")

    ''' 登录 登录过程只负责 验证账户/密码
        验证成功后 更新session
        失败则返回False
    '''

    def __login(self, username, password):
        with open(os.path.join(self.__DB_path, "DB_table", "user.json"), "r") as f:
            # print(f.read())
            userDict = json.load(f)
            print(userDict, "user.json")
            # if username in s:
            #     if s[username]["password"] == password:
            #         # Session()[username] = username
            #         # 修改用户状态
            #         # self.UserStatus(username, status=True)
            #         print("登录成功！")
            #         return True
            #     else:
            #         # Loggs().Error("用户不存在或密码错误！")
            #         print("用户名或密码不正确！")
            #         return False
            # else:
            #     print("非法用户！！！")
            #     return False
            if username in userDict:
                if userDict[username]["password"] == password:
                    pass
                    # Session()[username] = username  记录session

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
        self.__login(username,password)
