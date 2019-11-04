# -*- coding:utf-8 -*-
"""
   File Name:     html_downloader
   Description:   
   Author:        lsa
   date:          2019/9/29
"""
import urllib.request

import requests


class HtmlDownloader(object):
    """html下载器"""

    def download(self, url):
        if url is None:
            return
        headers_pc = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}
        response = requests.get(url,headers=headers_pc,timeout=10)
        if response.status_code != 200:
            return
        return response.content

