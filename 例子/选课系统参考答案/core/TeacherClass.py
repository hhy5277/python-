#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Henson

import time
from conf.settings import green, red, yellow, blue, magenta, white
from core.Baseclass import Baseclass
from core.SchoolPeople import SchoolPeople
# from core.main import Teacher_sys

class Teacher(SchoolPeople, Baseclass):  #多继承
    def __init__(self, name, password, age, sex, school_name):
        super(Teacher, self).__init__(name, password, age, sex) #重构父类SchoolPeople
        self.school_name = school_name
        self.grade_list = {}
        # self.class_list = {}
        self.class_record = []

        #读取班级数据
        teacher_list = self.readTeacherDb()
        teacher_list[self.name] = self

        #存储班级数据
        self.writeTeacherDb(teacher_list)

    def show_grade_info(self):
        """
        展示自己所教班级
        :return: 
        """
        print(magenta("您所教的班级如下:"))
        for _ in self.grade_list:
            print(blue(_))

    def create_class_record(self):
        """
        创建上课记录
        :return: 
        """
        while 1:
            print(magenta("您所教的班级如下".center(50, '-')))
            for _ in self.grade_list:
                print(blue(_))
            grade_name = input("请选择上课的班级<【b】返回>: ")
            if grade_name == 'b': break
            if grade_name in self.grade_list:
                break
            else:
                print(red("您输入班级有问题，请重新输入"))
                continue
        result_str = grade_name + time.strftime("%Y-%m-%d %X") + "上课记录"
        self.class_record.append(result_str)  #添加到班级记录列表中
        print(green("上课成功"))

        #读取班级数据
        teacher_list = self.readTeacherDb()
        teacher_list[self.name] = self

        #存储班级数据
        self.writeTeacherDb(teacher_list)

    @staticmethod
    def login():
        """
        教师登录验证
        :return: 
        """
        print(magenta("教师登录".center(40,'-')))
        teacher_all = Baseclass.readTeacherDb()  #读取所有教师信息
        username = input("请输入您的姓名: ").strip()
        if username in teacher_all:
            teacher_info = teacher_all[username]
            password = input("请输入您的密码: ").strip()
            if password in teacher_info.password:
                print(yellow("认证成功".center(40, '*')))
                return teacher_info
            else:
                print(red("您输入的密码有误,请重新输入!"))
        else:
            print(red("抱歉 老师 {} 不在本系统中".format(username)))

    def show_info(self):
        """
        显示老师信息
        :return: 
        """
        msg = """
        尊敬的教师：{name}, 您好, 您的详细信息如下：
        姓    名：{name}
        性    别：{sex}
        年    龄：{age}
        所在学校：{school}
        """.format(name=self.name, sex=self.sex, age=self.age, school=self.school_name)
        print(msg)
