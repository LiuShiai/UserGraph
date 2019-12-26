# -*- coding: utf-8 -*-
import re
from urllib.parse import unquote, urljoin

import scrapy
from scrapy import Request, Selector

from scrapyspider.items import ScrapyspiderItem
from spider.fetch_data import FetchData


class UserSpiderSpider(scrapy.Spider):
    name = 'user_spider'
    allowed_domains = ['baike.baidu.com']
    # start_urls = ['http://baike.baidu.com/']

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    #     'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9,image/webp, * / *;q = 0.8'}

    def start_requests(self):
        urls = FetchData().getUrls().new_urls
        print(len(urls))
        for key in urls.keys():
            for url in urls[key]:
                yield Request(url, callback=self.parse, dont_filter=True, meta={"key": key})

    def parse(self, response):
        key = response.meta['key']

        item = ScrapyspiderItem()
        a = re.compile(r'&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020|\t|\r')

        item['key'] = key
        item['flag'] = True

        if response.url == 'https://baike.baidu.com/error.html':
            item['flag'] = False

        item['title'] = response.xpath("//h1/text()").extract()[0]

        # item['key'] = response.xpath('//span[@class="viewTip-fromTitle"]//text()').extract()
        # if item['key'] is None:
        #     item['key'] = item['title']


        item['des'] = a.sub('', ''.join(response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]//h2//text()').extract())).strip('\n')
        item['summary'] = a.sub('', ''.join(response.xpath('//div[@class="lemma-summary"]//text()').extract())).strip('\n')
        basic_info = response.xpath('//div[@class="basic-info cmn-clearfix"]')
        bas = {}

        if basic_info:
            names = basic_info[0].xpath('.//dt[@class="basicInfo-item name"]').extract()
            values = basic_info[0].xpath('.//dd[@class="basicInfo-item value"]').extract()
            for i in range(len(names)):
                name = a.sub('', ''.join(Selector(text=names[i]).xpath('//dt//text()|//dt//a//text()').extract()))
                # br = Selector(text=values[i]).xpath('//br')
                # if br:
                #     pass
                v = a.sub('', ''.join(Selector(text=values[i]).xpath('//dd/text()|//dd//a//text()').extract()))
                v = v.strip('\n')
                value = v.replace('\n', ',')
                if name in bas.keys():
                    bas[name] = bas[name] + ',' + value
                else:
                    bas[name] = value
        item['basic_info'] = bas
        item['tag'] = a.sub('', ''.join(response.xpath('//div[@class="open-tag"]//dd//text()').extract()))
        poly = response.xpath('//div[@class="polysemant-list polysemant-list-normal"]').extract()
        if poly:
            li_urls = Selector(text=poly[0]).xpath('.//li').extract()
            if len(Selector(text=li_urls[0]).xpath('.//li//a').extract()) == 0:
                for i in range(1, len(li_urls)):
                    url = unquote(Selector(text=li_urls[i]).xpath('.//li//a//@href').extract()[0])
                    url = urljoin('https://baike.baidu.com/',url)
                    yield Request(url, dont_filter=True, callback=self.parse, meta={'key': key})

        yield item
