#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Henson

import os
import sys
from core.common import time_format
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

#定义好颜色函数
from termcolor import colored
green = lambda x:colored(x,'green')
red = lambda x:colored(x,'red')
yellow = lambda x:colored(x,'yellow')
blue = lambda x:colored(x,'blue')
magenta = lambda x:colored(x,'magenta')
white = lambda x:colored(x,'white')

AUTHOR = "henson"
GENDER = ["男", "male", "女", "female"]

DATA_PATH = os.path.join(BASE_DIR, 'db')
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
COURSE_PATH = os.path.join(DATA_PATH, "course.txt")    # 课程数据存放路径
SCHOOL_PATH = os.path.join(DATA_PATH, "school.txt")    # 学校数据存放路径
TEACHER_PATH = os.path.join(DATA_PATH, "teacher.txt")  # 教师数据存放路径
GRADE_PATH = os.path.join(DATA_PATH, "grade.txt")      # 班级数据存放路径
STUDENT_PATH = os.path.join(DATA_PATH, "student.txt")  # 学生数据存放路径


#管理员账号密码
ROOT_NAME = 'admin'
ROOT_PASSWD = 'admin'

#主菜单字典
main_dict = {
    '1': 'Admin.manage_sys',
    '2': 'Teacher_Sys.teacher_sys',
    '3': 'Student_Sys.student_sys',
}

# 管理员系统菜单
master_dict = {
    "1": "Admin().add_del_school",
    "2": "Admin().add_del_teacher",
    "3": "Admin().add_course",
    "4": "Admin().add_class",
    "5": "Admin().show_school",
    "6": "Admin().show_teacher",
    "7": "Admin().show_course",
    "8": "Admin().show_student"
}

# 教师系统菜单
teacher_dict = {
    "1": "Teacher_Sys.show_teacher",
    "2": "Teacher_Sys.show_grade",
    "3": "Teacher_Sys.create_class",
    # "4": "modify_score"
}


# 学生系统菜单
student_main_dict = {
    '1': 'Student_Sys().student_register',
    '2': 'Student_Sys().student_login',
}

# 学生登录系统后菜单
student_dict = {
     "1": "Student_Sys().show_student",
     "2": "Student_Sys().student_pay_tuition",
     # "3": "student_pay_homework",
 }

# 主菜单打印信息
msg_main = """
--------------- 欢迎进入选课系统 ----------------
Author: 【{name}】   当前日期: {time}

【1】  管理员系统
【2】  教师系统
【3】  学生系统
--------------------------------------------------
""".format(name=AUTHOR, time=time_format())

# 管理员系统打印信息
msg_master = """
--------------- 欢迎进入管理员界面 ----------------
当前日期: {time}

【1】  创建/删除 学校
【2】  创建 讲师
【3】  创建课程
【4】  创建班级
【5】  查看学校
【6】  查看讲师
【7】  查看课程
【8】  查看学生
--------------------------------------------------
""".format(time=time_format())

# 教师系统打印信息
msg_teacher = """
--------------- 欢迎进入教师界面 ----------------
当前日期: {time}

【1】  查询个人信息
【2】  查询所管班级
【3】  选择班级上课
--------------------------------------------------
""".format(time=time_format())

 # 学生系统打印信息
msg_student_main = """
--------------- 欢迎进入学生系统 ----------------
当前日期: {time}
 
【1】  注册
【2】  登录系统
 --------------------------------------------------
""".format(time=time_format())

# 学生登录系统后打印信息
msg_student = """
--------------- 欢迎学生界面 ----------------
当前日期: {time}

【1】  查询个人详情
【2】  交学费
--------------------------------------------------
""".format(time=time_format())
