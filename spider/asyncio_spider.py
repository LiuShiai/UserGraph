# -*- coding:utf-8 -*-
"""
   File Name:     process_spider
   Description:   
   Author:        lsa
   date:          2019/10/12
"""
import asyncio
import time
from multiprocessing import cpu_count
from multiprocessing.pool import Pool

import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote

from spider.fetch_data import FetchData


class UrlSpider(object):
    def __init__(self):
        self.urls = FetchData().getUrls()
        self.htmls = []
        self.sem = asyncio.Semaphore(10)
        self.failed_urls = []
        self.no_cont_urls = []

    # async def fetch(self, session, key, url):
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    #         'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}
    #     try:
    #         async with session.request('GET', url, headers=headers, verify_ssl=False) as resp:
    #             html = await resp.read()
    #             self.htmls.append((key, html))
    #             print('异步获取%s下的html。' % url)
    #     except Exception:
    #         print(f"error, {key}, {url}")
    #         self.failed_urls.append(key)

    #提交请求获取网页html
    async def get_html(self, key, url):
        code = 'utf-8'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}
        with(await self.sem):
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.request('GET', url, headers=headers, timeout=10, verify_ssl=False) as resp:
                        html = await resp.read()
                        self.htmls.append((key, html))
                        print('异步获取%s下的html。'% url)
                except:
                    print(f"error, {key}, {url}")
                    self.failed_urls.append(key)

    #协程调用方，请求网页
    def main_get_html(self):
        print(len(self.urls.new_urls))
        loop = asyncio.get_event_loop()
        tasks = [self.get_html(key, url) for key in self.urls.new_urls.keys() for url in self.urls.new_urls[key]]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    #使用多进程解析html
    def multi_parse_html(self, key, html, cnt):
        add_urls = set()
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find('title').contents[0]
        if title == '百度百科——全球最大中文百科全书':
            self.no_cont_urls.append(key)
        else:
            before = soup.find("div", class_="polysemant-list polysemant-list-normal")
            if before is not None:
                item_list = before.find_all('li')
                for i in range(1, len(item_list)):
                    a = item_list[i].find('a')
                    if a:
                        url = unquote(a['href'])
                        add_urls.add(urljoin('https://baike.baidu.com/', url))
                self.urls.update_urls(key, add_urls)
        print('第%d个html完成解析-add_urls:%d' % (cnt, len(add_urls)))

    #多进程调用总函数，解析html
    def main_parse_html(self):
        p = Pool(cpu_count())
        print(cpu_count())
        i = 0
        for key, html in self.htmls:
            i += 1
            p.apply_async(self.multi_parse_html, args=(key, html, i))
        p.close()
        p.join()


if __name__ == "__main__":
    start = time.time()
    task = UrlSpider()
    task.main_get_html()
    print('总url：%d' % (len(task.htmls)))
    print('失败url：%d' %(len(task.failed_urls)))
    task.main_parse_html()
    print(len(task.urls.new_urls))
    print(len(task.failed_urls))
    print('总耗时：%.5f秒' % float(time.time()-start))