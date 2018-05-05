# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/5/1 0001

import optparse
import socket
import json
import os
import shelve


class FTPClient:
    """
    ftp客户端
    """
    MSG_SIZE = 1024  # 消息最大长度1024

    def __init__(self):
        self.username = None
        self.terminal_display=None
        self.current_dir=None
        self.shelve_obj=shelve.open(".luffy_db")
        parser = optparse.OptionParser()
        parser.add_option("-s", "--server", dest="server", help="ftp server ip_adr")
        parser.add_option("-p", "--port", type="int", dest="port", help="ftp server port")
        parser.add_option("-u", "--username", dest="username", help="username info")
        parser.add_option("-P", "--password", dest="password", help="password info")
        self.options, self.args = parser.parse_args()
        print(self.options, self.args)
        self.args_verrification()

        self.make_connection()

    def args_verrification(self):
        """python 控制台参数 合法性检测"""

        if not self.options.server or not self.options.port:
            exit("必须提供 server 和 port 参数")

    def make_connection(self):
        """创建socket连接"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.options.server, self.options.port))


    def unfinished_file_check(self):
        """检查shelve db 把没有传完的文件列表打印，按用户指令决定是否重传"""
        print(list(self.shelve_obj.keys()),"?????")
        if list(self.shelve_obj.keys()):
            print("unfinished file list")
            for index, abs_file in enumerate(self.shelve_obj.keys()):
                received_file_size = os.path.getsize(self.shelve_obj[abs_file][1])
                print("%s . %s %s %s %s" % (index, abs_file,
                                            self.shelve_obj[abs_file][0],
                                            received_file_size,
                                            received_file_size / self.shelve_obj[abs_file][0] * 100))

            while True:
                choice = input("选择序号重新下载>>").strip()
                if not choice:continue
                if choice=="back":break
                if choice.isdigit():
                    choice=int(choice)
                    if choice>=0 and choice<=index:
                        selected_file = list(self.shelve_obj.keys())[choice]
                        print("tell server to resend file",selected_file)
                        self.send_msg("re_get",file_size=self.shelve_obj[selected_file][0],
                                      received_size=os.path.getsize(self.shelve_obj[selected_file][1]),
                                      abs_filename=selected_file)

                        response = self.get_response()

                        if response.get("status_code")==401:
                            local_filename =self.shelve_obj[selected_file][1]

                            with open(local_filename,"ab") as f:
                                total_size =self.shelve_obj[selected_file][0]
                                recv_size =os.path.getsize(self.shelve_obj[selected_file][1])
                                while recv_size<total_size:
                                    if total_size-recv_size<8192:
                                        data =self.sock.recv(total_size-recv_size)
                                    else:
                                        data =self.sock.recv(8192)
                                    recv_size+=len(data)
                                    f.write(data)
                                    print(recv_size,total_size)
                                else:
                                    print("file re_get down")

                            os.rename(local_filename, local_filename.replace(".download", ""))
                            del self.shelve_obj[selected_file, "%s.download" % selected_file]

                        else:
                            print(response.get("status_msg"))









    def interactive(self):
        """ 处理FTPserver 的所有交互"""

        # 首先处理登录验证
        if self.auth():
            self.unfinished_file_check()

            while True:
                user_input = input(self.terminal_display).strip()
                if not user_input: continue

                # 解析指令
                cmd_list = user_input.split()
                if hasattr(self, "_%s" % (cmd_list[0])):
                    func = getattr(self, "_%s" % (cmd_list[0]))
                    func(cmd_list[1:])  # get/put 后面跟的参数

    def parameter_check(self, args, min_args=None, max_args=None, exact_args=None):
        if min_args:
            if len(args) < min_args:
                print("必须提供至少%s个参数，只提供了%s个" % (min_args, len(args)))
                return False

        if max_args:
            if len(args) > max_args:
                print("最多提供%s个参数，提供了%s个" % (max_args, len(args)))
                return False

        if exact_args:
            if len(args) != exact_args:
                print("提供%s个参数，提供了%s个" % (max_args, len(args)))
                return False

        return True

    def send_msg(self, action_type, **kwargs):
        """
        客户端打包消息发送到服务器
        :param action_type:
        :param kwargs:
        :return:
        """
        msg_data = {
            "action_type": action_type,
            "fill":""
        }
        msg_data.update(kwargs)
        bytes_msg = json.dumps(msg_data).encode()
        if self.MSG_SIZE > len(bytes_msg):
            msg_data["fill"] = msg_data["fill"].zfill(self.MSG_SIZE - len(bytes_msg))
            bytes_msg = json.dumps(msg_data).encode()
        self.sock.send(bytes_msg)

    def progress_bar(self,total_size):

        current_percent=0
        last_percent=0
        received_size=0
        while True:
            received_size=yield current_percent
            current_percent = int(received_size/total_size *100)
            if current_percent>last_percent:
                print("#" * current_percent + "{percent}%".format(percent=current_percent),end="\r")
                last_percent = current_percent





    def _cd(self,cmd_args):
        """切换用户目录  cmd_args 是一个list"""
        if self.parameter_check(cmd_args,exact_args=1):
            target_dir =cmd_args[0]
            self.send_msg("cd",target_dir=target_dir)
            response = self.get_response()
            print(response)
            if response.get("status_code")==350:  #目录切换成功
                self.terminal_display="[\%s]"%response.get("current_dir")
                self.current_dir = response.get("current_dir")



    def _ls(self,cmd_args):
        """
        展示文件列表
        :return:
        """
        self.send_msg(action_type="ls")
        response = self.get_response()  #长度1024 只包含数据头
        print(response)
        if response.get("status_code")==302:
            cmd_result_size =response.get("cmd_result_size")

            received_size=0
            cmd_result =b""
            while received_size<cmd_result_size:
                if cmd_result_size-received_size<8192:
                    data=self.sock.recv(cmd_result_size-received_size)
                else:
                    data=self.sock.recv(8192)
                cmd_result+=data
                received_size+=len(data)
            else:
                print(cmd_result.decode("gbk"))






    def _get(self, cmd_args):
        """
        从服务器下载文件
        1、拿到文件名发送到服务器、
        2、等待服务器返回消息
            2.1、如果文件存在，返回文件大小，循环接收
            2.2、如果文件不存在，print status_msg

        """
        if self.parameter_check(cmd_args, min_args=1):
            filename = cmd_args[0]
            self.send_msg(action_type="get", filename=filename)  # 发送数据
            response = self.get_response()
            print(response,"???")
            if response.get("status_code") == 301:
                file_size = response.get("file_size")

                received_size = 0
                # f =open(filename,"wb")
                progress_generator=self.progress_bar(file_size)
                progress_generator.__next__()


                #save shelve db
                file_abs_path=os.path.join(self.current_dir,filename)
                print(file_abs_path,"----key----")
                self.shelve_obj[file_abs_path]=[file_size,"%s.download"%filename]

                with open("%s.download"%filename,"wb") as f:
                    while received_size<file_size:
                        if file_size-received_size<8192:
                            data =self.sock.recv(file_size-received_size)
                        else:
                            data=self.sock.recv(8192)
                        received_size+=len(data)
                        f.write(data)
                        progress_generator.send(received_size)
                        # print(received_size,file_size)
                    else:
                        print("\n")
                        print("文件%s接收完成，接收大小：%s"%(filename,received_size))
                        del self.shelve_obj[file_abs_path,"%s.download"%filename]
                        os.rename("%s.download"%filename,filename)
            else:
                print("文件不存在！")

    def _put(self, cmd_args):
        """上传本地文件到服务器
        获取服务器返回的数据1、确保本地文件存在 2、文件名和文件size放大消息头发到远程
        3、打开文件发送数据（不做文件覆盖处理）
        """
        if self.parameter_check(cmd_args,exact_args=1):
            local_file = cmd_args[0]
            if os.path.isfile(local_file):
                total_size=os.path.getsize(local_file)
                self.send_msg("put",file_size=total_size,filename=local_file)
                with open(local_file,"rb") as f:
                    uploaded_size = 0
                    last_percent=0
                    for line in f:
                        self.sock.send(line)
                        uploaded_size+=len(line)
                        current_percent=int(uploaded_size/total_size * 100)
                        if current_percent>last_percent+2:
                            print("#"*current_percent+"{percent}%".format(percent=current_percent),end="\r")
                            last_percent=current_percent


                    else:
                        print("\n")
                        print("100% 文件上传完成")


    def get_response(self):
        """
        :return:
        """
        data = self.sock.recv(self.MSG_SIZE).decode()
        return json.loads(data)

    def auth(self):
        count = 0
        while count < 3:
            username = input("username:").strip()
            if not username: continue
            password = input("password:").strip()

            cmd = {
                "action_type": "auth",
                "username": username,
                "password": password,
            }
            self.sock.send(json.dumps(cmd).encode("utf-8"))
            response = self.get_response()
            print(response, "response")
            if response.get("status_code") == 200:
                self.username = username
                self.terminal_display="[%s] :>>" % self.username
                self.current_dir=''
                return True
            else:
                print(response.get("status_msg"))
                count += 1


if __name__ == '__main__':
    client = FTPClient()
    client.interactive()
