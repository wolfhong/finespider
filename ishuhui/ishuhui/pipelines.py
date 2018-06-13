# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hashlib import md5
from scrapy.exceptions import DropItem
from ishuhui.models import SessionContext, Book, Chapter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class IshuhuiPipeline(object):
    pass
