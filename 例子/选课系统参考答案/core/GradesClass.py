#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Henson

from core.Baseclass import Baseclass

class Grades(Baseclass):
    def __init__(self, grade_name, course_name, teacher_name):
        self.grade_name = grade_name
        self.course_name = course_name
        self.teacher_name = teacher_name
        self.student_list = {}

        #读取班级数据
        grade_list = self.readCourseDb()
        grade_list[self.grade_name] = self

        #存储班级数据
        self.writeCourseDb(grade_list)
