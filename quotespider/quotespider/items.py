# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from quotespider.models import Quote
from quotespider.model2item import create_item_cls


QuoteItem = create_item_cls(Quote)
