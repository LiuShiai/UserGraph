# -*- coding:utf-8 -*-
"""
   File Name:     User
   Description:   定义结点集对应实体类
   Author:        lsa
   date:          2019/9/29
"""
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

from dao.neo4j import Neo4j


class User(GraphObject):
    __primarylabel__ = "user"
    __primarykey__ = "userid"

    name = Property()
    userid = Property()
    groupid = Property()


class PlayWorks(GraphObject):
    __primarylabel__ = "PlayWorks"
    __primarykey__ = "tid"

    title = Property()
    tid = Property()

    roles = RelatedFrom('User', '登场作品')


user = User()
user.name = "佐助"
user.userid = 3
# user2 = User()
# user2.name = "shy"
# user2.userid = 2
works = PlayWorks()
works.title = "网球王子"
# works.roles.add(user)
graph = Neo4j().graph
# graph.push(user)
graph.push(works)
print(user.__ogm__.node)
