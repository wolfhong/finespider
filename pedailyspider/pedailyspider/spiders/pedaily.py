# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pedailyspider.items import INVItem, IPOItem, MAItem, PEItem


class PedailySpider(CrawlSpider):
    name = 'pedaily'
    allowed_domains = ['zdb.pedaily.cn']
    start_urls = [
        'http://zdb.pedaily.cn/inv/p1/',
        'http://zdb.pedaily.cn/ipo/p1/',
        'http://zdb.pedaily.cn/ma/p1/',
        'http://zdb.pedaily.cn/pe/p1/',
    ]
    rules = [
        Rule(LinkExtractor(allow=(r'/inv/p\d+/', )), callback='parse_inv'),
        Rule(LinkExtractor(allow=(r'/ipo/p\d+/', )), callback='parse_ipo'),
        Rule(LinkExtractor(allow=(r'/ma/p\d+/', )), callback='parse_ma'),
        Rule(LinkExtractor(allow=(r'/pe/p\d+/', )), callback='parse_pe'),
    ]

    def format_url(self, response, url):
        return response.urljoin(url) if url else url

    def parse_inv(self, response):
        for event in response.xpath('//ul[@id="inv-list"]/li'):
            item = INVItem()
            item['date_str'] = event.css("span.time::text").extract_first()
            if not item['date_str']:
                yield item

            item['company'] = event.css(".company a::text").extract_first()
            item['company_url'] = self.format_url(response, event.css(".company a::attr(href)").extract_first())

            item['industry'] = event.css(".industry a::text").extract_first()
            item['industry_url'] = self.format_url(response, event.css(".industry a::attr(href)").extract_first())

            item['money_stage'] = event.css(".money span.r::text").extract_first()
            item['money_spans'] = ''.join(event.css(".money span::text").extract())
            item['group_nolink'] = event.css(".group span::text").extract()
            item['group_text'] = event.css(".group a::text").extract()
            item['group_href'] = event.css(".group a::attr(href)").extract()
            item['view_url'] = self.format_url(response, event.css(".view a::attr(href)").extract_first())
            yield item

    def parse_ipo(self, response):
        for event in response.xpath('//url[@id="ipo-list"]/li'):
            item = IPOItem()
            item['date_str'] = event.css("span.time::text").extract_first()
            if not item['date_str']:
                yield item

            item['company'] = event.css(".company a::text").extract_first()
            item['company_url'] = self.format_url(response, event.css(".company a::attr(href)").extract_first())

            item['industry'] = event.css(".industry a::text").extract_first()
            item['industry_url'] = self.format_url(response, event.css(".industry a::attr(href)").extract_first())

            item['money_spans'] = ''.join(event.css(".money span::text").extract())
            item['place'] = event.css(".place a::text").extract_first()
            item['place_url'] = self.format_url(response, event.css(".place a::attr(href)").extract_first())

            item['view_url'] = self.format_url(response, event.css(".view a::attr(href)").extract_first())
            yield item

    def parse_ma(self, response):
        for event in response.xpath('//url[@id="ma-list"]/li'):
            item = MAItem()
            item['date_str'] = event.css("span.time::text").extract_first()
            if not item['date_str']:
                yield item

            item['company'] = event.css(".company a::text").extract_first()
            item['company_url'] = self.format_url(response, event.css(".company a::attr(href)").extract_first())

            item['industry'] = event.css(".industry a::text").extract_first()
            item['industry_url'] = self.format_url(response, event.css(".industry a::attr(href)").extract_first())

            item['money_spans'] = ''.join(event.css(".money span::text").extract())
            item['company2'] = event.css(".company2 a::text").extract_first()
            item['company2_url'] = self.format_url(response, event.css(".company2 a::attr(href)").extract_first())

            item['view_url'] = self.format_url(response, event.css(".view a::attr(href)").extract_first())
            yield item

    def parse_pe(self, response):
        for event in response.xpath('//url[@id="pe-list"]/li'):
            item = PEItem()
            item['date_str'] = event.css("span.time::text").extract_first()
            if not item['date_str']:
                yield item

            item['fund'] = event.css(".fund a::text").extract_first()
            item['fund_url'] = self.format_url(response, event.css(".fund a::attr(href)").extract_first())

            group = (event.css(".group::text").extract_first() or '').strip()
            if group:
                group_url = None
            else:
                group = event.css(".group a::text").extract_first()
                group_url = event.css(".group a::attr(href)").extract_first()
            item['group'] = group
            item['group_url'] = self.format_url(response, group_url)

            item['money_spans'] = ''.join(event.css(".money span::text").extract())
            item['view_url'] = self.format_url(response, event.css(".view a::attr(href)").extract_first())
            yield item
