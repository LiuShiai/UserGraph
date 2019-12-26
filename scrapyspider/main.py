# -*- coding:utf-8 -*-
"""
   File Name:     main
   Description:   
   Author:        lsa
   date:          2019/10/15
"""
import os
import sys

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.basename(__file__)))

execute(['scrapyspider', 'crawl', 'user_spider'])

