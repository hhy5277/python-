# -*- coding:utf-8 -*-
# AUTHER   @ Alvin
import logging
import os

class Loggs(object):
    '''
        日志记录
        logging.basicConfig(filename='example.log',level=logging.INFO)
        logging.debug('This message should go to the log file')
        logging.info('So should this')
        logging.warning('And this, too')
    '''
    def __init__(self):
        self.__logpath = os.path.abspath("") + "/log/"
        # 实例化log对象
        self.__ch = logging.getLogger("log")
        # 全局设置记录日志级别
        self.__ch.setLevel(logging.INFO)
    #所有日志
    def All(self, content):
        all_log =  logging.FileHandler(self.__logpath + 'All.log')
        all_log.setLevel(logging.NOTSET)
        self.__ch.addHandler(all_log)
        file_formater = logging.Formatter(
            "%(asctime)s %(message)s %(levelno)s %(levelname)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d %(message)s")
        all_log.setFormatter(file_formater)
        self.__write(content)

    # 错误日志
    def Error(self, content):
        errors_lgo = logging.FileHandler(self.__logpath + 'error.log')
        errors_lgo.setLevel(logging.WARNING)
        self.__ch.addHandler(errors_lgo)
        file_formater = logging.Formatter(
            "%(asctime)s %(message)s %(levelno)s %(levelname)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d %(message)s")
        errors_lgo.setFormatter(file_formater)
        self.__write(content)

    # 金融交易日志
    def Finance(self, content):
        finance = logging.FileHandler(self.__logpath + 'Finance.log')
        finance.setLevel(logging.CRITICAL)
        self.__ch.addHandler(finance)
        file_formater = logging.Formatter("%(asctime)s %(levelno)s %(message)s")
        finance.setFormatter(file_formater)
        self.__write(content)


    def __write(self, content):
        self.__ch.critical(content)
        self.__ch.warning(content)
        self.__ch.error(content)
        self.__ch.debug(content)
        self.__ch.info(content)

