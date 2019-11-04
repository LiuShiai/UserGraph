# -*- coding:utf-8 -*-
"""
   File Name:     xmongo
   Description:   连接mongo数据库
   Author:        LJY
   date:          2019-05-05
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import pymongo
from bson import ObjectId
from config import *


class XMongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)

    @staticmethod
    def check_param(query, colname, db):
        if None in [query, colname, db]:
            raise Exception("Please specify query/col/db.")

    def get_db(self):
        db = self.client[database]
        return db

    def get_col(self, db, colname):
        db = self.client[db]
        col = db[colname]
        return col

    def query(self, query=None, colname=None, db='ml'):
        self.check_param(query, colname, db)
        col = self.get_col(db, colname)
        cursors = col.find(query)
        return cursors

    def insert(self, query=None, colname=None, db='ml'):
        self.check_param(query, colname, db)
        col = self.get_col(db, colname)
        col.insert_one(query)



if __name__ == '__main__':
    task = XMongo()
    cur = task.query(query={"_id": ObjectId("564da77ffbe78e53a0ca057f")}, colname='user')
    for c in cur:
        print(c['name'])

    col = task.get_col(database,colname)
    cr = col.find({'_id':ObjectId("564da77ffbe78e53a0ca057f")},{'description':1,'groupid':1,'name':1})
    for c in cr:
        print(c)