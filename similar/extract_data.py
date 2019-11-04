# -*- coding:utf-8 -*-
"""
   File Name:     extract_data
   Description:   
   Author:        lsa
   date:          2019/10/10
"""
import glob
import json
import os

from bs4 import BeautifulSoup

from dao.xmongo import XMongo
from similar.des_similar import DesSimilar


class ExtractData(object):
    def __init__(self):
        self.db = XMongo().get_db()
        self.db_data = {}
        self.spider_data = {}

    def getUser(self, groupid):
        userList = []
        users = self.db["user"].find({"groupid": groupid}, {"name": True, "description": True, "status": True, "groupid": True})
        for user in users:
            if user.get("status", -1) == -1:
                continue
            userList.append(user)
        return userList

    #从数据库中获取名人数据
    def fetch_data_from_db(self):
        userList = self.getUser(2)
        print(len(userList))
        for u in userList:
            name = u.get('name')
            self.db_data.setdefault(name, [])
            self.db_data[name].append(u)
        print(len(self.db_data))

    # 从爬取的百度百科库中获取名人数据
    def fetch_data_from_spider(self):
        path = '../data/group2_item.txt'
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                row = json.loads(line)
                key, value = list(row.items())[0]
                self.spider_data.setdefault(key, [])
                if len(value) > 0:
                    self.spider_data[key].append(value)
        print(len(self.spider_data))

    def match_user(self):
        simTask = DesSimilar()
        simTask.load_stopwords_list()  # 加载停用词库
        simTask.load_jieba_userdict()  # 加载自定义词库
        for key in self.db_data.keys():
            users = self.db_data[key]
            spiders = self.spider_data[key]
            print(users)
            print(spiders)
            print(len(users))
            print(len(spiders))
            if len(spiders) > 0:
                users = DesSimilar().match_user_spider(users, spiders)
            print(users)


if __name__ == "__main__":
    task = ExtractData()
    task.fetch_data_from_db()
    task.fetch_data_from_spider()
    task.match_user()










