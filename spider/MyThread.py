# -*- coding:utf-8 -*-
"""
   File Name:     MyThread
   Description:   
   Author:        lsa
   date:          2019/9/30
"""
import threading
class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self._running = True
        self.name = name

    def terminate(self):
        self._running = False

    def run(self):
        pass