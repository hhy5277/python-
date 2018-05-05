# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/5/1 0001
import socket, os
from conf import setting
import json, hashlib
import configparser
import subprocess
import time


class FTPServer:
    STATUS_CODE = {
        200: "Passed authentication",
        201: "Wrong username or password",
        300: "File not exist",
        301: "File exist  including file size",
        302: "this msg including msg size",
        350: "dir changed success",
        351: "dir not exist",
        401: "file exist, ready to resend",
        402: "File exist ,but file size not match"
    }
    MSG_SIZE = 1024  # 消息最大长度1024

    def __init__(self, management_instance):
        self.management_instance = management_instance
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((setting.HOST, setting.PORT))
        self.sock.listen(5)
        self.request = None
        self.addr = None
        self.accounts = self.load_accounts()
        self.user_obj = None
        self.user_current_dir = None

    def run_forever(self):
        print("starting server at %s:%s" % (setting.HOST, setting.PORT))
        while True:  # 链接循环
            print("开始一个accept")
            self.request, self.addr = self.sock.accept()  # 在这里等待
            # accept只是建立一个连接，连接完成后可以循环recv()数据
            print(self.addr)
            try:
                self.handle()
            except Exception as e:
                print("handle处理过程发送错误，",e)
                self.request.close()


    def handle(self):
        while True:  # 某一个链接上的循环
            try:
                raw_data = self.request.recv(self.MSG_SIZE)  # 此处需要优化 1024接收cmd指令
                if not raw_data:
                    print("客户端链接断开")
                    self.request = None
                    self.addr = None
                    break
                data = json.loads(raw_data.decode("utf-8"))
                action_type = data.get("action_type")
                if action_type:
                    if hasattr(self, "_%s" % (action_type)):  # _ 开头的都是与客户端进行交互的
                        func = getattr(self, "_%s" % (action_type))
                        func(data)  # data {}
                    else:
                        print("不合法action_type1")
                else:
                    print("不合法action_type")
            except ConnectionError:
                print("window conn 断开")
                break

    def send_response(self, status_code, *args, **kwargs):
        """
        打包发送消息给客户端
        :param status_code:
        :param args:
        :param kwargs: {filename:"aaa"}
        :return:
        """
        data = kwargs
        data["status_code"] = status_code
        data["status_msg"] = self.STATUS_CODE[status_code]
        data["fill"] = ""
        bytes_data = json.dumps(data).encode("utf-8")

        if len(bytes_data) < 1024:
            data["fill"] = data["fill"].zfill(1024 - len(bytes_data))
            bytes_data = json.dumps(data).encode()

        self.request.send(bytes_data)



    def _put(self,data):
        """客户端上传文件到服务器"""

        local_file = data.get("filename")
        full_path=os.path.join(self.user_current_dir,local_file)
        if os.path.isfile(full_path):
            full_name="%s.%s"%(full_path,time.time())
        else:
            full_name=full_path

        total_size=data.get("file_size")
        received_size = 0
        with open(full_name,"wb") as f:
            while received_size<total_size:
                try:
                    if total_size - received_size < 8192:
                        data = self.request.recv(total_size - received_size)
                    else:
                        data = self.request.recv(8192)
                    if not data:
                        print("上传文件客户端断开 data没有数据")
                        break
                    received_size += len(data)
                    f.write(data)
                    print(received_size, total_size)
                except ConnectionError:
                    print("上传文件客户端断开")
                    break
            else:
                print("文件：%s 接收完成"%local_file)


    def _cd(self, data):
        """根据用户的target_dir 改变用户的self.user_current_dir

        """
        target_dir = data.get("target_dir")
        full_path = os.path.abspath(os.path.join(self.user_current_dir, target_dir))
        print(full_path)
        if os.path.isdir(full_path):
            if full_path.startswith(self.user_obj["home"]):
                self.user_current_dir = full_path
                relative_current_dir = self.user_current_dir.replace(self.user_obj["home"], "")
                self.send_response(350, current_dir=relative_current_dir)
            else:
                self.send_response(351)
        else:
            self.send_response(351)

    def _ls(self, data):
        """获取client dir指令 返回结果"""
        cmd_obj = subprocess.Popen("dir %s" % self.user_current_dir, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout = cmd_obj.stdout.read()
        stderr = cmd_obj.stderr.read()
        cmd_obj.stdout.close()
        cmd_obj.stderr.close()
        cmd_result = stdout + stderr
        if not cmd_result:
            cmd_result = "当前文件夹下没文件"
        self.send_response(302, cmd_result_size=len(cmd_result))
        self.request.sendall(cmd_result)

    def _re_get(self,data):
        """send file to client"""
        print("re_get",data)
        abs_filename=data.get("abs_filename")
        print(abs_filename)
        print(abs_filename.strip("\\"))
        full_path =os.path.join(self.user_obj["home"],abs_filename.strip("\\"))
        if os.path.isfile(full_path):
            if os.path.getsize(full_path)== data.get("file_size"):
                self.send_response(401)
                with open(full_path,"rb") as f:
                    f.seek(data.get("received_size"))
                    for line in f:
                        self.request.send(line)
            else:
                self.send_response(402,sile_size_on_server =os.path.getsize(full_path))
        else:
            self.send_response(300)

    def _get(self, data):
        """下载文件"""
        filename = data.get("filename")
        full_path = os.path.join(self.user_current_dir, filename)
        if os.path.isfile(full_path):
            filesize = os.path.getsize(full_path)
            self.send_response(301, file_size=filesize)
            print("准备下载")
            with open(full_path, "rb") as f:
                for line in f:
                    self.request.send(line)

        else:
            self.send_response(300)

    def _auth(self, data):
        """处理客户端用认证"""
        print("auth :", data)
        if self.authenticate(data.get("username"), data.get("password")):
            print("_auth 验证通过")
            # 返回标准数据格式
            self.send_response(status_code=200)
        else:
            self.send_response(status_code=201)

    def load_accounts(self):
        """加载用户信息"""
        config_obj = configparser.ConfigParser()
        config_obj.read(setting.ACCOUNT_FILE)
        # print(config_obj.sections())
        # print(config_obj)
        # print(config_obj["alex"])
        # print(config_obj["alex"]["name"])

        # cfg.items(SECTION)
        # print(config_obj.has_section("alex"),"????")
        return config_obj

    def authenticate(self, username, password):
        if self.accounts.has_section(username):
            _password = self.accounts[username]['password']
            md5_obj = hashlib.md5()
            md5_obj.update(password.encode("utf-8"))
            md5_password = md5_obj.hexdigest()
            print("md5 password:", md5_password)
            if md5_password == _password:
                print("验证通过")
                self.user_obj = self.accounts[username]
                self.user_obj["home"] = os.path.join(setting.USER_HOME_DIR, username)  # 家目录
                self.user_current_dir = self.user_obj["home"]
                return True
            else:
                print("密码错误")
                return False
        else:
            print("密码错误2")
            return False
