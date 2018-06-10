# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class INVItem(scrapy.Item):
    date_str = scrapy.Field()
    company = scrapy.Field()
    company_url = scrapy.Field()
    industry = scrapy.Field()
    industry_url = scrapy.Field()

    money_stage = scrapy.Field()
    money_spans = scrapy.Field()
    group_nolink = scrapy.Field()  # list
    group_text = scrapy.Field()  # list
    group_href = scrapy.Field()  # list
    view_url = scrapy.Field()


class IPOItem(scrapy.Item):
    date_str = scrapy.Field()
    company = scrapy.Field()
    company_url = scrapy.Field()
    industry = scrapy.Field()
    industry_url = scrapy.Field()

    money_spans = scrapy.Field()
    place = scrapy.Field()
    place_url = scrapy.Field()
    view_url = scrapy.Field()


class MAItem(scrapy.Item):
    date_str = scrapy.Field()
    company = scrapy.Field()
    company_url = scrapy.Field()
    industry = scrapy.Field()
    industry_url = scrapy.Field()

    money_spans = scrapy.Field()
    company2 = scrapy.Field()
    company2_url = scrapy.Field()
    view_url = scrapy.Field()


class PEItem(scrapy.Item):
    date_str = scrapy.Field()
    fund = scrapy.Field()
    fund_url = scrapy.Field()
    group = scrapy.Field()
    group_url = scrapy.Field()

    money_spans = scrapy.Field()
    view_url = scrapy.Field()
