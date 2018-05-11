#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Henson

from core.Baseclass import Baseclass

class Course(Baseclass):  #单继承
    def __init__(self, name, course_cycle, course_price, school_name):
        self.name = name
        self.course_cycle = course_cycle
        self.course_price = course_price
        self.school_name = school_name

        #读取课程数据
        course_list = self.readCourseDb()
        course_list[self.name] = self

        #存储课程数据
        self.writeCourseDb(course_list)
