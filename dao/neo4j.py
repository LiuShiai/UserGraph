# -*- coding:utf-8 -*-
"""
   File Name:     neo4j
   Description:   
   Author:        lsa
   date:          2019/9/29
"""
from py2neo import Graph, Node, Relationship
from config import *


class Neo4j(object):
    def __init__(self):
        self.graph = Graph(NEO_URI, username=username, password=password)

