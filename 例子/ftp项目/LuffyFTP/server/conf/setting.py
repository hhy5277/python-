# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/5/1 0001

import os
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST ="127.0.0.1"
PORT =8080

ACCOUNT_FILE = "%s/conf/accounts.ini" % BASE_DIR
USER_HOME_DIR=os.path.join(BASE_DIR,"home")
