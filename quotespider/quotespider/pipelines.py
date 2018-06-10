# -*- coding: utf-8 -*-
from hashlib import md5
from scrapy.exceptions import DropItem
from quotespider.models import SessionContext
from quotespider.items import QuoteItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QuotespiderPipeline(object):

    def __init__(self):
        self.digest_set = set()
        self.insert_list = []
        self.insert_count = 10

    def process_item(self, item, spider):
        _map = {
            'quote': self.process_quote,
        }
        method = _map.get(spider.name, None)
        if method:
            return method(item, spider)

    def process_quote(self, item, spider):
        item['digest'] = md5(item['content'].encode('utf8')).hexdigest()
        digest = item['digest']
        if digest in self.digest_set:
            raise DropItem("Duplicate item found: %s" % item)
        self.digest_set.add(digest)
        self.insert_list.append(QuoteItem.item2model(item))
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
