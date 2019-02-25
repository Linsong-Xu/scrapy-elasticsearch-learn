# -*- coding: utf-8 -*-
# @Time    : 2019-02-25 11:07
# @Author  : xls56i

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
print(os.path.join(BASE_DIR, "static"))
