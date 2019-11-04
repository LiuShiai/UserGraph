# -*- coding:utf-8 -*-
"""
   File Name:     UrlManager
   Description:   
   Author:        lsa
   date:          2019/9/29
"""


class UrlManager(object):
    """url 管理器，避免重复爬取"""
    def __init__(self):
        self.new_urls = {}
        self.old_urls = {}

    def get_new_url(self):
        """获取待爬取得新url"""
        key, new_urls = self.new_urls.popitem()
        old_urls = self.old_urls.get(key, set())
        self.old_urls[key] = old_urls | new_urls
        return key, new_urls

    def update_urls(self, key, urls):
        if key is None:
            return
        self.new_urls[key] = urls

    def add_new_url(self, key, url):
        """添加解析的新的url"""
        if key is None or url is None:
            return
        if url not in self.new_urls.get(key, set()) and url not in self.old_urls.get(key, set()):
            new_urls = self.new_urls.get(key, set())
            new_urls.add(url)
            self.new_urls[key] = new_urls

    def add_new_urls(self, key, urls):
        """添加解析到得新的urls列表"""
        if key is None or urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(key, url)

    def has_new_url(self):
        """判断是否有新的待爬取的url"""
        if self.new_urls:
            return True
        return False


if __name__ == "__main__":
    url = {"name": {1,2}, "age": {2,3}}
    o_url = {}
    if o_url:
        print(True)
