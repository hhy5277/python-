# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/5/1 0001
from core import main

class ManagementTool:
    def __init__(self,sys_argv):
        self.sys_argv = sys_argv
        print(sys_argv)

    def verify_argv(self):
        if len(self.sys_argv)<2:
            self.help_msg()
        if not hasattr(self.sys_argv[1]):
            self.help_msg()


    def help_msg(self):
        msg ="""
            start    start FTP server
            stop     stop  FTP server 
            restart  restart FTP server
            createUser  username create a ftp user
        """
        exit(msg)

    def execute(self):
        cmd =self.sys_argv[1]
        func = getattr(self,cmd)
        func()


    def start(self):
        server = main.FTPServer(self)  #把当前的managementTool实例传入到FTPServer对象中
        server.run_forever()



