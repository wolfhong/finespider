# -*- coding: utf-8 -*-
import scrapy


def _item2model(cls, item):
    return item._model(**item._values)


def create_item_cls(model, name=None, excludes=None, includes=None, extras=None):
    if not name:
        name = '{}{}'.format(model.__name__, 'Item')
    extras = extras or []
    excludes = excludes or []
    includes = includes or []

    kw = {}
    for key in model.__dict__.keys():
        if not key.startswith('_'):
            if includes:
                if key in includes:
                    kw[key] = scrapy.Field()
            elif excludes:
                if key not in excludes:
                    kw[key] = scrapy.Field()
            else:
                if key not in ['id']:
                    kw[key] = scrapy.Field()
    for key in extras:
        kw[key] = scrapy.Field()
    kw['_model'] = model
    kw['item2model'] = classmethod(_item2model)
    return type(name, (scrapy.Item, ), kw)
