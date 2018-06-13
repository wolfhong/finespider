# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    cartoon = scrapy.Field()
    url = scrapy.Field()


class ChapterItem(scrapy.Item):
    cartoon = scrapy.Field()
    chapter = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
