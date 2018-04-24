# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/15 0015

# 红色31  蓝色34
def print_red(msg):
    print('\033[1;31m  [%s] \033[0m' % msg)


def print_blue(msg):
    print('\033[1;34m  [%s] \033[0m' % msg)


def print_green(msg):
    print('\033[1;32m  [%s] \033[0m' % msg)
