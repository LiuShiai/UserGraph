# -*- coding:utf-8 -*-
"""
   File Name:     fetch_data
   Description:   
   Author:        lsa
   date:          2019/10/10
"""
import json
import os

from bs4 import BeautifulSoup
from bson import ObjectId

from dao.xmongo import XMongo
from spider.url_manager import UrlManager


class FetchData(object):
    def __init__(self):
        self.db = XMongo().get_db()
        self.userList = []

    def getUser(self, groupid):
        users = self.db["user"].find({"groupid": groupid}, {"name": True, "description": True, "status": True})
        for user in users:
            if user.get("status", -1) == -1:
                continue
            self.userList.append(user)

    def getUrls(self):
        # 获取游戏动漫中角色
        self.getUser(2)
        urls = UrlManager()
        print(len(self.userList))
        i = 6
        start = 0*10000
        end = (i+1)*10000
        if end > len(self.userList):
            end = len(self.userList)
        for user in self.userList[start:end]:
            userid = user["_id"]
            # userid = ObjectId("55755d29fbe78e45909ae1fe")
            name = user["name"].split('/')[0]
            # name = '紫'
            url = "https://baike.baidu.com/item/" + name
            # key = "{userid}_{name}".format(userid=userid, name=name)
            key = user["name"]
            urls.add_new_url(key, url)
        return urls


    def write_no_spider_user(self):
        #将直接百度没有得到内容的user保存下来
        print(len(self.no_spider))
        if len(self.no_spider) == 0:
            return
        path = "../data/no_spider.txt"
        with open(path, 'a', encoding='utf-8') as f:
                for user in self.no_spider:
                    try:
                        f.writelines("{_id}\t{name}\t{des}\n".format(
                            _id=user["_id"],
                            name=user["name"],
                            des=user["description"]
                        ))
                    except Exception as e:
                            print(user)
                            print(e)



    def parser_html(self):
        path = "../data/item_html"
        filelist = os.listdir(path)
        for i in range(len(filelist)):
            id_name = filelist[i][:-4].split('_')
            userid = ObjectId(id_name[0])
            name = id_name[1]
            html_cont = open(os.path.join(path, filelist[i]), 'r', encoding='utf-8')


if __name__ == "__main__":
    urls = FetchData().getUrls()
    print(len(urls.new_urls))