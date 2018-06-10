# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hashlib import md5
from scrapy.exceptions import DropItem
from pedailyspider.models import SessionContext

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


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
        company = item.get('company', None) or item.get('fund', None)
        return md5((date_str + company).encode('utf8')).hexdigest()

    def process_item(self, item, spider):
        if item.__class__.__name__ != self.ITEM_CLASSNAME:
            return
        if not item['date_str']:
            raise DropItem()
        digest = self.build_digest()
        if digest in self.digest_set:
            raise DropItem("Duplicate item found: %s" % item)
        self.digest_set.add(digest)
        self.insert_list.append(self.item_to_model(item))
        if len(self.insert_list) < self.insert_count:
            return
        with SessionContext() as session:
            session.add_all(self.insert_list)
            session.commit()
            self.insert_list = []

    def close_spider(self, spider):
        if self.insert_list:
            with SessionContext() as session:
                session.add_all(self.insert_list)
                session.commit()
                self.insert_list = []


class INVPipeline(BasePipeline):
    ITEM_CLASSNAME = 'inv'


class IPOPipeline(BasePipeline):
    ITEM_CLASSNAME = 'ipo'


class MAPipeline(BasePipeline):
    ITEM_CLASSNAME = 'ma'


class PEPipeline(BasePipeline):
    ITEM_CLASSNAME = 'pe'
