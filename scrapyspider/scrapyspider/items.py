# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    key = scrapy.Field()
    flag = scrapy.Field()
    title = scrapy.Field()
    des = scrapy.Field()
    summary = scrapy.Field()
    basic_info = scrapy.Field()
    tag = scrapy.Field()
