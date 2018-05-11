#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Henson

import time

from core.Baseclass import Baseclass
from core.SchoolPeople import SchoolPeople
from conf.settings import green, red, yellow, blue, magenta, white

class Student(SchoolPeople, Baseclass): #多继承
    """学生类"""
    def __init__(self, name, password, age, sex, class_name, course_name,school_name, tuition, pay=0):
        super().__init__(name, password, age, sex)
        self.class_name = class_name
        self.course_name = course_name
        self.school_name = school_name
        self.tuition = tuition
        self.pay = pay

        #读取学生数据
        student_list = self.readStudentDb()
        student_list[self.name] = self

        #存储学生数据
        self.writeStudentDb(student_list)

    def pay_tuition(self):
        """支付学费"""
        if self.pay == 1:
            print(green("学费已交，无需再交"))
        else:
            print("您当前需要付学费: ", self.tuition, '元')
            while True:
                tuition_name = input("请输入您要交的学费: ").strip()
                if tuition_name.isdigit() and (int(tuition_name) - int(self.tuition) >= 0):
                    print(blue("学费已交，谢谢"))
                    self.pay = 1

                    #写入学生数据
                    student_info = self.readSchoolDb() #先读数据
                    student_info[self.name] = self  #再更新数据
                    self.writeStudentDb(student_info) #保存数据
                    return True
                else:
                    print(red("您输入学费不够支付"))

    def show_info(self):
        """展示个人信息"""
        msg = """
        ----- 亲爱的同学 {name} 你好，你详细信息如下-----
            姓    名:  {name}
            性    别:  {sex}
            年    龄:  {age}
            所在学校:  {school}
            所在班级:  {grade}
        """.format(name=self.name, sex=self.sex, age=self.age, school=self.school_name, grade=self.class_name)
        print(blue(msg))

    @staticmethod
    def login():
        print(magenta("学生登录".center(40,"-")))
        student_all = Baseclass.readStudentDb()
        name = input("请输入您的姓名: ").strip()
        if name in student_all:
            student_info = student_all[name]
            password = input("请输入您的密码: ").strip()
            if password == student_info.password:
                print(yellow("登录成功"))
                return student_info
            else:
                print("您输入的密码有误")
        else:
            print(red("抱歉 学生 %s 在本系统中不存在" % name))