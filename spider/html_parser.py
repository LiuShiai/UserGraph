# -*- coding:utf-8 -*-
"""
   File Name:     html_parser
   Description:   
   Author:        lsa
   date:          2019/9/29
"""
import json
import os
import re
from urllib.parse import urljoin, unquote

from bs4 import BeautifulSoup
from lxml.html.clean import unicode


class HtmlParser(object):
    """html解析器"""
    def parser(self, key, html):
        if html is None:
            return
        soup = BeautifulSoup(html, 'lxml')
        new_urls = self._get_new_urls(soup)
        is_saved = self._save_html_data(key, soup, html)
        return new_urls, is_saved

    def _get_new_urls(self, soup):
        sets = set()
        #查找多义词url
        before = soup.find("div", class_="polysemant-list polysemant-list-normal")
        if before is not None:
            item_list = before.find_all('li')
            a = item_list[0].find('a')
            if a is None:
                for i in range(1, len(item_list)):
                    a = item_list[i].find('a')
                    if a:
                        url = unquote(a['href'])
                        sets.add(urljoin('https://baike.baidu.com/', url))
        return sets

    def _save_html_data(self, key, soup, html_cont):
        is_saved = False
        if key is None:
            return
        # path = os.path.join('../data/item_html1', key)
        path = '../data/item_html_p.txt'
        # if not os.path.exists(path):
        #     os.mkdir(path)
        title = soup.find('title').contents[0]
        dataset = {}

        # with open(os.path.join(path, title + '.html'), 'w', encoding='utf-8') as f:
        #     f.write(html_cont.decode('utf-8'))
        if title != '百度百科——全球最大中文百科全书':
            soup = soup.find("div", class_="main-content")
            title_des = soup.find('dd', class_='lemmaWgt-lemmaTitle-title')
            if title_des:
                if title_des.find('h1'):
                    dataset['title'] = title_des.find('h1').get_text()
                if title_des.find('h2'):
                    dataset['des'] = title_des.find('h2').get_text()
            if soup.find("div", class_="lemma-summary"):
                dataset['summary'] = "".join(soup.find("div", class_="lemma-summary").stripped_strings)
            basic_info = soup.find("div", class_="basic-info")
            if basic_info:
                names = basic_info.find_all("dt", class_="basicInfo-item name")
                values = basic_info.find_all("dd", class_="basicInfo-item value")
                b_infos = {}
                a = re.compile(r'\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t|\r')
                for i in range(len(names)):
                    name = names[i].get_text()
                    name = a.sub('', name)
                    value = "".join(values[i].stripped_strings)
                    b_infos[name] = value
                dataset['basic_info'] = b_infos
            if soup.find(id='open-tag-item'):
                dataset['tag'] = "".join(soup.find(id='open-tag-item').stripped_strings)

        content = {key: dataset}
        with open(os.path.join(path), 'a', encoding='utf-8') as f:
            try:
                f.writelines(json.dumps(content, ensure_ascii=False) + '\n')
                # f.write("{title}\n{des}\n{summary}\n{basic_info}\n{tag}".format(
                #     title=dataset['title'],
                #     des=dataset['des'],
                #     summary=dataset['summary'],
                #     basic_info=dataset['basic_info'],
                #     tag=dataset['tag']
                # ))
            except Exception as e:
                print(e)
                print(dataset)
        return is_saved



