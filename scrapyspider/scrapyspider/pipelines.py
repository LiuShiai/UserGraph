# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os


class ScrapyspiderPipeline(object):
    def process_item(self, item, spider):
        dataset = {}
        flag = item['flag']
        if flag:
            dataset['title'] = item['title']
            dataset['des'] = item['des']
            dataset['summary'] = item['summary']
            dataset['basic_info'] = item['basic_info']
            dataset['tag'] = item['tag']
        content = {item['key']: dataset}
        with open("../data/group2_item.txt", 'a', encoding='utf-8') as f:
            f.writelines(json.dumps(content, ensure_ascii=False) + '\n')
        return item['key']
