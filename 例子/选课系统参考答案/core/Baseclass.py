#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Henson

import os
import pickle
from conf import settings


class Baseclass():
    """
    基础类，主要包括文件的读写操作
    """
    def __init__(self):
        pass

    @staticmethod
    def readSchoolDb():
        if os.path.exists(settings.SCHOOL_PATH):
            if os.path.getsize(settings.SCHOOL_PATH) > 0:  #判断文件大小
                school_info = pickle.load(open(settings.SCHOOL_PATH, 'rb'))
            else:
                school_info = {}
        else:
            school_info = {}
        return  school_info

    @staticmethod
    def writeSchoolDb(info):
        pickle.dump(info, open(settings.SCHOOL_PATH, 'wb'))
        # with open(settings.SCHOOL_PATH, 'wb')as f_school:
        #     pickle.dump(info, f_school)

    @staticmethod
    def readTeacherDb():
        if os.path.exists(settings.TEACHER_PATH):
            if os.path.getsize(settings.TEACHER_PATH) > 0:
                teacher_info = pickle.load(open(settings.TEACHER_PATH, 'rb'))
            else:
                teacher_info = {}
        else:
            teacher_info = {}
        return teacher_info

    @staticmethod
    def writeTeacherDb(info):
        pickle.dump(info, open(settings.TEACHER_PATH, 'wb'))

    @staticmethod
    def readStudentDb():
        if os.path.exists(settings.STUDENT_PATH):
            if os.path.getsize(settings.STUDENT_PATH) > 0:
                student_info = pickle.load(open(settings.STUDENT_PATH,'rb'))
            else:
                student_info = {}
        else:
            student_info = {}
        return student_info

    @staticmethod
    def writeStudentDb(info):
        pickle.dump(info, open(settings.STUDENT_PATH,'wb'))

    @staticmethod
    def readCourseDb():
        if os.path.exists(settings.COURSE_PATH):
            if os.path.getsize(settings.COURSE_PATH) > 0:
                course_info = pickle.load(open(settings.COURSE_PATH, 'rb'))
            else:
                course_info = {}
        else:
            course_info = {}
        return course_info

    @staticmethod
    def writeCourseDb(info):
        pickle.dump(info, open(settings.COURSE_PATH, 'wb'))

    @staticmethod
    def readGradeDb():
        if os.path.exists(settings.GRADE_PATH):
            if os.path.getsize(settings.GRADE_PATH) > 0:
                grade_info = pickle.load(open(settings.GRADE_PATH, 'rb'))
            else:
                grade_info = {}
        else:
            grade_info = {}
        return grade_info

    @staticmethod
    def writeGradeDb(info):
        pickle.dump(info, open(settings.GRADE_PATH, 'wb'))