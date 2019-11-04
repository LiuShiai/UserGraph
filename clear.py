# -*- coding:utf-8 -*-
"""
   File Name:     clear
   Description:   
   Author:        lsa
   date:          2019/10/12
"""

import psutil
import os


info = psutil.virtual_memory()
print(u'内存使用：',psutil.Process(os.getpid()).memory_info().rss)
print(u'总内存：',info.total)
print(u'内存占比：',info.percent)
print(u'cpu个数：',psutil.cpu_count())