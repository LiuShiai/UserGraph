# -*- coding:utf-8 -*-
"""
   File Name:     spider_main
   Description:   
   Author:        lsa
   date:          2019/9/29
"""
import json
import os
import pickle
import sys
import time
import urllib



from dao.xmongo import XMongo
from spider import html_downloader, html_parser
from spider.fetch_data import FetchData
from spider.url_manager import UrlManager


import threading
# from gevent import monkey; monkey.patch_all(thread=False)


class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self._running = True
        self.name = name

    def terminate(self):
        self._running = False

    def run(self):
        pages = 0
        spendtime = 0
        while urls.has_new_url() and self._running:
            try:
                start = time.time()
                LOCK.acquire()
                key, new_urls = urls.get_new_url()
                LOCK.release()
                add_urls = set()
                for new_url in new_urls:
                    html_cont = downloader.download(new_url)
                    add_url, _ = parser.parser(key, html_cont, LOCK)
                    add_urls = add_urls | add_url
                    # except:
                    #     with open('../data/no_spider.txt', 'a', encoding='utf-8') as f1:
                    #         f1.writelines("{key}\t{url}\n".format(key=key, url=new_url))
                LOCK.acquire()
                urls.add_new_urls(key, add_urls)
                LOCK.release()
                pages += 1
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
    # PATH = '../data/urls.pkl'
    # urls = FetchData().getUrls()
    # LOCK = threading.Lock()
    # downloader = html_downloader.HtmlDownloader()
    # parser = html_parser.HtmlParser()
    #
    # threads = []
    # count_thread = 6
    # length = len(urls.new_urls)
    # print(f'build key urls, length={length}')
    # for i in range(count_thread):
    #     print(f'build thread {i}...')
    #     threads.append(MyThread(str(i)))
    # try:
    #     for t in threads:
    #         t.start()
    #         t.join()
    # except:
    #     for t in threads:
    #         t.terminate()
    #         print('error!', sys.exc_info()[0])
    # finally:
    #     print('finished, saving state')
    #     pickle.dump(urls, open(PATH, 'wb'))

    # path = "../data/item_html"
    # user = os.listdir(path)
    # print(len(user))
    cont = []
    with open('../data/group2_item.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            dic = json.loads(line)
            cont.append(dic)

    print(len(cont))
    new_dic = {}
    for i in range(len(cont)):
        for key in cont[i]:
            new_dic.setdefault(key, [])
            if len(cont[i][key]) > 0:
                new_dic[key].append(cont[i][key])
    print(len(new_dic))



