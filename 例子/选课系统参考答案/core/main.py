#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Henson

import os
import sys
import pickle
import time
from termcolor import colored
from conf.settings import green, red, yellow, blue, magenta, white
from conf import settings
from core.TeacherClass import Teacher
from core.Baseclass import Baseclass
from core.SchoolClass import School
from core.StudentClass import Student


#使用元类来控制类
class Mymeta(type):  #需要有type内建元类
    def __init__(self, class_name, class_bases, class_dic):
        if not class_name.istitle():
            raise TypeError("类名的首字母必须大写")
        if '__doc__' not in class_dic or not class_dic['__doc__'].strip():
            raise TypeError("必须有注释， 且注释不能为空")
        super(Mymeta, self).__init__(class_name, class_bases, class_dic)

#----------- 管理员类 ------------
class Admin(Baseclass, metaclass=Mymeta):
    """
    管理员类
    """
    def __init__(self):  #先占个位，留以后扩展
        pass

    @staticmethod
    def manage_sys():
        print(magenta("管理员登录".center(30,"-")))
        _username = input("请输入管理员姓名: ").strip()
        _password = input("请输入管理员密码: ").strip()
        if _username == settings.ROOT_NAME and _password == settings.ROOT_PASSWD:
            while 1:
                print(green(settings.msg_master))
                choice = input("请输入系统序列号<【b】返回 | 【q】退出>: ")
                if choice.lower() == 'b': break
                elif choice.lower() == 'q': exit("goodbye".center(50, "-"))
                else:
                    eval(settings.master_dict[choice])() if choice in settings.master_dict else print(red("抱歉输入编号不存在"))
        else:
            print(red('用户名或者密码错误'))

    def add_del_school(self):
        while 1:
            school_list = self.readSchoolDb()
            if len(school_list):
                print(magenta("目前开放的学校如下".center(50, '-')))
                for _ in school_list:
                    print(blue(_))
            school_name = input("请输入创建的学校名称 <【d】删除｜【b】返回>: ").strip()
            if school_name == 'b': break
            elif school_name == 'd':   #【d】删除
                if os.path.getsize(settings.SCHOOL_PATH) > 0:
                    with open(settings.SCHOOL_PATH, 'rb+') as f:
                        user_dict = pickle.load(f)
                        choice = input("删除相应的地址：")
                        if choice in user_dict:
                            user_dict.pop(choice)   #指定删除
                        else:
                            print(red("输入有误"))
                        dict = pickle.dumps(user_dict)
                        f.seek(0)
                        f.truncate(0)
                        f.write(dict)
                else:
                    print(red("当前文件是空"))
                    # break
            elif school_name in school_list:
                print(red("抱歉，当前 【{}】 校区已经存在，请勿重复创建.".format(school_name)))
                # break
            else:
                School(school_name)
                print(blue("【{}】 校区创建成功".format(school_name)))
                # break

    def add_del_teacher(self):
        while 1:
            school_all = self.readSchoolDb()
            if not len(school_all):
                print(red("暂时没有开放学校地址，请联系管理员【henson】")); break
            print(magenta('请选择您的学校地址： '.center(40, "-")))
            for _ in school_all:
                print(blue(_))
            choice_name = input("请输入上面选择的学校地址<【b】返回>: ").strip()
            if choice_name == 'b': break
            elif choice_name in school_all:
                school_obj = school_all[choice_name]
                school_obj.create_teacher()  #重点，触发了School类下的create_teacher()函数方法的Teacher()
                print(yellow("创建讲师成功"))
                break
            else:
                print(red("输入有误"))

    def add_course(self):
        while 1:
            school_all = self.readSchoolDb()
            print(magenta("请选择您的学校".center(40, "-")))
            for _ in school_all:
                print(_)
            choice = input("请输入选择的学校地址<【b】返回>: ").strip()
            if choice == 'b': break
            print(magenta("欢迎进入{} 校区".center(40,'-').format(choice)))
            if choice in school_all:
                school_obj = school_all[choice]
                school_obj.create_course()
                # print(yellow("创建课程成功"))
                break
            else:
                print(red("输入有误"))

    def add_class(self):
        school_all = self.readSchoolDb()
        while 1:
            print(magenta("请选择您的学校:".center(40, "-")))
            for _ in school_all:
                print(_)
            choice = input("请输入选择的学校名称<【b】返回>: ").strip()
            if choice == 'b': break
            if choice in school_all:
                school_obj = school_all[choice]
                school_obj.create_grades()
                # print(yellow("创建班级成功"))
                break
            else:
                print(red("输入有误"))

    def show_school(self):
        school_all = self.readSchoolDb()
        print(magenta("当前开放的学校地址：".center(40, "-")))
        for _ in school_all:
            print(blue(_))
        time.sleep(1)

    def show_teacher(self):
        teacher_all = self.readTeacherDb()
        # print(teacher_all)
        print(magenta("当前所有的教师".center(40, '-')))
        for teacher_name in teacher_all:
            print("""----------------------  讲师 ------------------------
                     姓    名:  {}
                     性    别:  {}
                     年    龄:  {}
                     所在学校:  {}
                     所在班级:  {}
                 """.format(teacher_all[teacher_name].name,
                            teacher_all[teacher_name].sex,
                            teacher_all[teacher_name].age,
                            teacher_all[teacher_name].school_name,
                            teacher_all[teacher_name].grade_list))

    def show_course(self):
        print(magenta("当前开放的课程：".center(40, "-")))
        student_all = self.readSchoolDb()
        for name in student_all:
            result = student_all[name].school_course_list
            for i in result:
                print("课程：", i)

    def show_student(self):
        print(magenta("当前注册的学生信息".center(40,"-")))
        student_all = self.readGradeDb()
        for name in student_all:
            # print(student_all[name].student_list)
            result = student_all[name].student_list
            for i in result:
                print("学生:\t{}".format(i))


#----------- 教师类 ------------
class Teacher_Sys(Baseclass, metaclass=Mymeta):
    """
    教师类
    """
    def __init__(self):
        pass

    # 教师系统
    @staticmethod
    def teacher_sys():
        teacher_obj = Teacher.login()  #先登录再执行下面的操作
        # print(teacher_obj)
        if teacher_obj:
            while 1:
                print(green(settings.msg_teacher))
                choice = input("请输入系统序列号<【b】返回 | 【q】退出>: ")
                if choice.lower() == 'b':
                    break
                elif choice.lower() == 'q':
                    exit("goodbye".center(50, "-"))
                else:
                    eval(settings.teacher_dict[choice])(teacher_obj) if choice in settings.teacher_dict else print(
                        red("抱歉输入编号不存在"))

    @staticmethod
    def show_teacher(obj):     #使用了多态指针
        obj.show_info()

    @staticmethod
    def show_grade(obj):     #使用了多态指针
        obj.show_grade_info()

    @staticmethod
    def create_class(obj):  #使用了多态指针
        obj.create_class_record()

#----------- 学生类 ------------
class Student_Sys(School, metaclass=Mymeta):
    """
    学生类
    """
    def __init__(self):
        pass

    @staticmethod
    def student_sys():  #学生菜单入口
        while 1:
            print(green(settings.msg_student_main))
            choice = input("请选择要进入的系统序号<【b】返回|【q】退出>: ").strip()
            if choice.lower() == 'b': break  #跳出循环
            elif choice.lower() == 'q': exit("goodbye".center(40, '-'))
            else:
                eval(settings.student_main_dict[choice])() if choice in settings.student_main_dict else print(red(
                    "Error,输入编号不存在!"))

    #学生注册
    def student_register(self):
        school_all = self.readSchoolDb()
        while 1:
            if not len(school_all):
                print(red("暂时没开放学校，请联系管理员"))
                break  #跳出循环
            print(magenta("当前开放的学校".center(40, '-')))
            for _ in school_all:
                print(blue(_))
            choice = input("请输入选择的学校名称<【b】返回>: ").strip()
            if choice.lower() == 'b': break
            elif choice in school_all:
                school_obj = school_all[choice]  #更新继承School类
                # print(school_obj.__dict__)
                school_obj.create_student()  #马上跳到School类下创建学生函数方法
                # self.create_student()  #等于School.create_student()
                break
            else:
                print(red("输入有误"))

    # 学生登录
    def student_login(self):
        student_obj = Student.login()
        if student_obj:
            while 1:
                print(green(settings.msg_student))
                choice = input("请选择要进入的系统序号< 【b】返回|【q】退出>: ").strip()
                if choice.lower() == 'b':break #退出循环
                elif choice.lower() == 'q': exit("goodbye".center(40, '-'))
                else:
                    eval(settings.student_dict[choice])(student_obj) if choice in settings.student_dict else print(red("抱歉输入编号不存在"))

    @staticmethod
    def show_student(obj):  #多态指针
        obj.show_info()

    @staticmethod
    def student_pay_tuition(obj):  #多态指针
        obj.pay_tuition()


#主入口
def run():
    while 1:
        # print(magenta("欢迎进入选课系统".center(50, '-')))
        print(green(settings.msg_main))
        choice = input("请输入系统序列号<【b】返回 | 【q】退出>: ")
        if choice.lower() == 'b': break
        elif choice.lower() == 'q': exit("goodbye".center(50, "-"))
        else:
            # 使用eval函数妙用
            eval(settings.main_dict[choice])() if choice in settings.main_dict else print(red("抱歉输入编号不存在"))