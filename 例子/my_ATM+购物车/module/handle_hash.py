# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/19 0019

import hashlib

class Handlehash(object):
    '''
        加密|解密 ：类
    '''
    def encode_hash(self, password):
        if isinstance(password, str):
            import hashlib
            hs = hashlib.sha1()
            hs.update(bytes(password, encoding="utf-8"))
            return hs.hexdigest()
        else:
            return False

    def decode_hash(self,new = None,old = None):
        new_pasd = self.Jam_hash(new)
        old_pasd = self.Jam_hash(old)
        if new_pasd == old_pasd:
            return True
        else:
            return False