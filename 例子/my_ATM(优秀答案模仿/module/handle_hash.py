# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/19 0019

import hashlib


class Handlehash:
    '''
        加密| ：类
    '''
    def __init__(self):
        pass

    def encode_hash_sha1(self, password):
        if isinstance(password, str):
            hs = hashlib.sha1()
            hs.update(bytes(password, encoding="utf-8"))
            return hs.hexdigest()
        else:
            return False
