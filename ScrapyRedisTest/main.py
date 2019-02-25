# -*- coding: utf-8 -*-
# @Time    : 2019-02-22 11:57
# @Author  : xls56i

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'jobbole'])
