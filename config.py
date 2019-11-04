# -*- coding:utf-8 -*-
"""
   File Name:     config
   Description:   
   Author:        lsa
   date:          2019/9/29
"""


#neo4j连接参数
NEO_URI = "http://localhost:7474"
username = "neo4j"
password = "642"

# ################# MONGO #################
# MONGO_URI = "mongodb://127.0.0.1:27017/ml"
#MONGO_URI = "mongodb://wechat_develop:wechat_develop@121.41.45.182:27017/wechat"
MONGO_URI = "mongodb://127.0.0.1:27017/"

# mongo数据库名称
database = 'matchservice'

# 自定义词典
userdict_filepath = '../dict/newdict.txt'

# 停用词表路径
stopwords_filepath = '../dict/stopwords.txt'
