#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Henson

from conf.settings import green, red, yellow, blue, magenta, white
from core.Baseclass import Baseclass
from conf import settings
from core.TeacherClass import Teacher
from core.CourseClass import Course
from core.GradesClass import Grades
from core.StudentClass import Student

class School(Baseclass):  #继承Baseclass所有属性
    """
    学校类"""
    def __init__(self, name):
        self.school_name = name
        self.school_course_list = {}
        self.school_teacher_list = {}
        self.school_grades_list = {}
        self.school_student_list = {}

        #读取学校数据
        school_list = self.readSchoolDb()
        school_list[self.school_name] = self

        #存储学校数据
        self.writeSchoolDb(school_list)

    def create_teacher(self):
        school_all = self.readSchoolDb()
        while 1:
            teacher_name = input("请输入教师姓名: ").strip()
            if teacher_name in school_all[self.school_name].school_teacher_list:
                print(red("抱歉该 【{}】 校区的【{}】 老师已经存在，请勿重复创建".format(self.school_name, teacher_name)))
            else:
                break
        teacher_password = input("请输入教师登录密码: ").strip()
        teacher_age = input("请输入教师年龄: ").strip()
        teacher_sex = input("请输入教师性别: ").strip()
        school_name = self.school_name   #更新

        #创建教师对象
        teacher_obj = Teacher(teacher_name, teacher_password, teacher_age, teacher_sex, school_name)

        #读取教师数据
        teacher_info = self.readTeacherDb()
        teacher_info[teacher_name] = teacher_obj  #重点，main.py交互逻辑文件中的Admin类需要要调用下面的School类的Techer()方法

        #存储教师数据
        self.writeTeacherDb(teacher_info)

        self.school_teacher_list[teacher_name] = teacher_name
        #读取学校数据
        school_list = self.readSchoolDb()
        school_list[self.school_name] = self

        #存储学校数据
        self.writeSchoolDb(school_list)
        print(blue("""----- 恭喜注册成功 【 {name} 】 老师注册详细信息如下----- 
                        姓    名：{name}
                        密    码：{pwd}
                        年    龄：{age}
                        性    别：{sex}
                        所在学校：{school}
                        请妥善保存好您的信息
        """.format(name=teacher_name, pwd=teacher_password, age=teacher_age, sex=teacher_sex,
                   school=school_name)))

    def show_teacher(self):
        teacher_info = self.readTeacherDb()
        print("teacher_info = ", teacher_info.__dict__)

    def create_course(self):
        """创建课程"""
        while 1:
            school_all = self.readSchoolDb()
            print(magenta("当前校区，开放的课程如下".center(40,'-')))
            for _ in school_all[self.school_name].school_course_list:
                print(blue("开放的课程 >> {}".format(_)))
            course_name = input("请输入课程名称: ").strip()
            course_cycle = input("请输入课程周期: ").strip()
            course_price = input("请输入课程价格: ").strip()

            # 创建课程对象
            course_obj = Course(course_name, course_cycle, course_price, self.school_name)

            # 读取课程数据
            course_info = self.readCourseDb()
            course_info[course_name] = course_obj

            # 存储课程信息
            # self.writeCourseDb(course_info)
            self.school_course_list[course_name] = course_name  #更新到school_course_list字典里面保存先

            # 读取学校数据先做判断是否存在
            school_list = self.readSchoolDb()
            if course_name in school_all[self.school_name].school_course_list:
                print(red("抱歉，你的课程【{}】已经存在，创建失败".format(course_name)))
                break

            # 存储学校数据
            school_list[self.school_name] = self
            self.writeCourseDb(course_info)
            self.writeSchoolDb(school_list)
            print(blue("""----- 恭喜注册成功 【 {name} 】 课程注册详细信息如下----- 
                            课程名字：{name}
                            课程周期：{cycle}
                            课程价格：{price}
                            所在学校：{school}
                            请妥善保存好您的信息
            """.format(name=course_name, cycle=course_cycle, price=course_price,school=self.school_name)))
            break

    def create_grades(self):
        """创建班级"""
        teacher_info = self.readTeacherDb()  #读取教师数据
        grade_name = input("请输入班级名称: ").strip()
        #选择教师
        while 1:
            print(magenta("请选择本校老师: ".center(40,'-')))
            for _ in self.school_teacher_list:
                print(yellow(_))
            teacher_name = input("请输入你要选择的老师姓名: ").strip()
            if teacher_name not in self.school_teacher_list:
                print(red("输入的有误"))
            else:
                break
        #选择课程
        while 1:
            print(magenta("请选择本校课程：".center(40, '-')))
            for _ in self.school_course_list:
                print(yellow(_))
            grade_course = input("请输入你要选择的课程名称: ").strip()
            if grade_course not in self.school_course_list:
                print(red("输入的有误"))
            else:
                break
        # 创建班级对象
        grade_obj = Grades(grade_name, grade_course,teacher_name)

        #写入学校班级数据库
        self.school_grades_list[grade_name] = grade_name

        #先读取学校数据
        school_list = self.readSchoolDb()
        #再存储学校数据
        school_list[self.school_name] = self
        self.writeSchoolDb(school_list)

        #写入教师数据库
        teacher_info[teacher_name].grade_list[grade_name] = grade_name
        self.writeTeacherDb(teacher_info)

        # 写入班级数据库
        grade_info = self.readGradeDb()
        grade_info[grade_name] = grade_obj
        self.writeGradeDb(grade_info)

    def create_student(self):
        """创建学生"""
        while 1:
            print(magenta("创建学生".center(40, '-')))
            name = input("请输入您的姓名: ").strip()
            password = input("请输入您的密码: ").strip()
            while 1:
                print(blue(" --> 年龄必须是大于0整数"))
                age = input("请输入您的年龄: ").strip()
                if age.isdigit():
                    if not int(age) >= 0:
                        print(red("--> 年龄必须是大于0"))
                    else:
                        break
                else:
                    print(red(" --> 年龄必须是整数"))
            while 1:
                print(blue("--> 性别你只能输入以下可选选项"))
                for _ in settings.GENDER:
                    print(_, end=" | ")
                print("")
                sex = input("请输入您的性别: ").strip()
                if sex in settings.GENDER: break   #如果sex存在就跳过
            #读班级数据
            grade_list = self.readGradeDb()
            #读学校数据
            school_list = self.readSchoolDb()
            print(magenta("该校区目前可选择班级信息如下: ".center(40,'-')))
            for _ in school_list[self.school_name].school_grades_list:
                print(_)

            grade_name = input("请输入要注册班级名称: ").strip()
            if grade_name in grade_list:
                if name in grade_list[grade_name].student_list:
                    print(red("抱歉该班级学生 {} 已经存在,新增学生失败".format(name)))
                    break
            else:
                print(red("您输入的班级名称有问题"))
                break

            grade_obj = grade_list[grade_name]   #更新
            grade_obj.student_list[name] = name  #更新
            grade_list[grade_name] = grade_obj   #再更新

            #写入班级学生列表
            self.writeGradeDb(grade_list)

            #读班级课程数据
            course_all = self.readCourseDb()
            # course_price = course_all[grade_obj.course_name].price
            course_price = course_all[grade_obj.course_name].course_price

            #创建学生对象
            student_obj = Student(name, password, age, sex, grade_name, grade_obj.course_name, self.school_name,course_price)

            #写入数据
            student_all = self.readStudentDb()  #先读出数据
            student_all[name] = student_obj  #更新
            self.writeStudentDb(student_all)  #写入数据

            msg = """----- 恭喜注册成功 【 {name} 】 同学注册详细信息如下----
                姓   名: {name}
                密   码: {pwd}
                年   龄: {age}
                性   别: {sex}
                学   校: {school}
                班   级: {grade} 
                请妥善保存好您的信息
            """.format(name=name, pwd=password, age=age, sex=sex, school=self.school_name, grade=grade_name)
            print(blue(msg))
            break