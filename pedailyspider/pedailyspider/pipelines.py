# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from hashlib import md5
from scrapy.exceptions import DropItem
from pedailyspider.models import SessionContext, IPOModel, INVModel

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# 还是会有解析错误的情况
def str_to_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y年%m月%d日').date()
    except ValueError:
        try:
            return datetime.datetime.strptime(date_str, '%Y年%m月').date()
        except ValueError:
            try:
                return datetime.datetime.strptime(date_str, '%Y%m%d').date()
            except ValueError:
                return datetime.date(1900, 1, 1)


class BasePipeline(object):
    ITEM_CLASSNAME = None

    def __init__(self):
        self.digest_set = set()
        self.insert_list = []
        self.insert_count = 200
        assert self.ITEM_CLASSNAME

    def item_to_model(self, item):
        raise NotImplementedError

    def build_digest(self, item):
        date_str = item['date_str']
        company = item.get('company', None) or item.get('fund', None) or ''
        return md5((date_str + company).encode('utf8')).hexdigest()

    def process_item(self, item, spider):
        if item.__class__.__name__ != self.ITEM_CLASSNAME:
            return item
        if not item['date_str']:
            raise DropItem("Error item: %s" % item)
        digest = self.build_digest(item)
        if digest in self.digest_set:
            raise DropItem("Duplicate item found: %s" % item)
        self.digest_set.add(digest)
        self.insert_list.append(self.item_to_model(item))
        if len(self.insert_list) >= self.insert_count:
            with SessionContext() as session:
                session.add_all(self.insert_list)
                session.commit()
                self.insert_list = []
        raise DropItem("Used item: %s" % item)

    def close_spider(self, spider):
        if self.insert_list:
            with SessionContext() as session:
                session.add_all(self.insert_list)
                session.commit()
                self.insert_list = []


class INVPipeline(BasePipeline):
    ITEM_CLASSNAME = 'INVItem'

    def item_to_model(self, item):
        model = INVModel()
        model.date_str = item['date_str']
        model.date = str_to_date(item['date_str'])
        model.company = item['company'] or ''
        model.company_url = item['company_url'] or ''
        model.category = item['industry'] or ''
        model.money_stage = item['money_stage'] or ''
        model.money_spans = item['money_spans'] or ''
        model.investors = '/'.join(item['group_nolink'] + item['group_text'])
        model.about = item['view_url'] or ''
        return model


class IPOPipeline(BasePipeline):
    ITEM_CLASSNAME = 'IPOItem'

    def item_to_model(self, item):
        model = IPOModel()
        model.date_str = item['date_str']
        model.date = str_to_date(item['date_str'])
        model.company = item['company'] or ''
        model.company_url = item['company_url'] or ''
        model.category = item['industry'] or ''
        model.money_spans = item['money_spans'] or ''
        model.place = item['place'] or ''
        model.place_url = item['place_url'] or ''
        model.about = item['view_url'] or ''
        return model


class MAPipeline(BasePipeline):
    ITEM_CLASSNAME = 'MAItem'


class PEPipeline(BasePipeline):
    ITEM_CLASSNAME = 'PEItem'
