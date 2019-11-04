# -*- coding:utf-8 -*-
"""
   File Name:     Process_spider
   Description:   
   Author:        lsa
   date:          2019/10/14
"""
import json
import os
import pickle
import sys
import time
import urllib
from multiprocessing import Process, cpu_count, Lock, Queue, freeze_support
from gevent.pool import Pool as ge_pool

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from spider import html_downloader, html_parser
from spider.fetch_data import FetchData
from spider.url_manager import UrlManager



import threading
# from gevent import monkey; monkey.patch_all(thread=False)


class MyProcess(Process):
    def __init__(self, name, urls_deq, lock):
        Process.__init__(self)
        self._running = True
        self.name = name
        self.urls_deq = urls_deq
        self.lock = lock

    def terminate(self):
        self._running = False

    def crawling_web(self, key, url):
        html_cont = downloader.download(url)
        add_url, _ = parser.parser(key, html_cont)
        self.lock.acquire()
        for u in add_url:
            self.urls_deq.put((key, u))
        self.lock.release()

    def run(self):
        pages = 0
        spendtime = 0
        greenlet_pool = ge_pool(10)
        while not self.urls_deq.empty and self._running:
            try:
                start = time.time()
                self.lock.acquire()
                key, new_url = self.urls_deq.get()
                self.lock.release()
                greenlet_pool.apply_async(self.crawling_web, (key, new_url, ))
                spendtime += time.time() - start
                cost = spendtime / pages
                print(f"Thread: {self.name} key:{key}, {str(cost)[:4]}:sec/page")
            except KeyboardInterrupt:
                print('save state', sys.exc_info())
                pickle.dump(urls, open('../data/urls.bin', 'wb'))
            except:
                continue


if __name__ == "__main__":
    # 获取游戏动漫中角色
    PATH = '../data/urls.pkl'
    urls = FetchData().getUrls()

    lock = Lock()
    url_deq = Queue()
    print(url_deq.qsize())
    for key in urls.new_urls.keys():
        for url in urls.new_urls[key]:
            url_deq.put((key, url))
    print(url_deq.qsize())
    downloader = html_downloader.HtmlDownloader()
    parser = html_parser.HtmlParser()

    pool = []
    count_process = cpu_count()
    length = len(urls.new_urls)
    print(f'build key urls, length={length}')
    freeze_support()
    for i in range(count_process):
        print(f'build process {i}...')
        p = MyProcess(str(i), url_deq, lock)
        pool.append(p)
        p.start()
    try:
        for p in pool:
            p.join()
    except:
        for p in pool:
            p.terminate()
            print('error!', sys.exc_info()[0])
    finally:
        print('finished, saving state')
        # pickle.dump(urls, open(PATH, 'wb'))

    # path = "../data/item_html"
    # user = os.listdir(path)
    # print(len(user))
    # cont = []
    # with open('../data/item_html.txt', 'r', encoding='utf-8') as f:
    #     for line in f.readlines():
    #         dic = json.loads(line)
    #         cont.append(dic)
    #
    # new_dic = {}
    # for i in range(len(cont)):
    #     for key in cont[i]:
    #         new_dic.setdefault(key, [])
    #         if len(cont[i][key]) > 0:
    #             new_dic[key].append(cont[i][key])
    # print(len(new_dic))

