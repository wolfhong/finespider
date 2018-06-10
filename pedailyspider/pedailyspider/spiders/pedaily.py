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
        # 'http://zdb.pedaily.cn/ma/p1/',
        # 'http://zdb.pedaily.cn/pe/p1/',
    ]
    rules = [
        Rule(LinkExtractor(allow=(r'/inv/p\d+/', )), callback='parse_inv'),
        Rule(LinkExtractor(allow=(r'/ipo/p\d+/', )), callback='parse_ipo'),
        # Rule(LinkExtractor(allow=(r'/ma/p\d+/', )), callback='parse_ma'),
        # Rule(LinkExtractor(allow=(r'/pe/p\d+/', )), callback='parse_pe'),
    ]

    def format_url(self, response, url):
        return response.urljoin(url) if url else url

    def get_company_and_url(self, response, event, classname):
        company = (event.css(".%s::text" % classname).extract_first() or '').strip()
        if company:
            company_url = None
        else:
            company = event.css(".%s a::text" % classname).extract_first()
            company_url = event.css(".%s a::attr(href)" % classname).extract_first()
        return company, self.format_url(response, company_url)

    def parse_inv(self, response):
        for event in response.xpath('//ul[@id="inv-list"]/li'):
            item = INVItem()
            item['date_str'] = event.css("span.time::text").extract_first()
            if not item['date_str']:
                yield item

            item['company'], item['company_url'] = self.get_company_and_url(response, event, 'company')
            item['industry'], item['industry_url'] = self.get_company_and_url(response, event, 'industry')

            item['money_stage'] = event.css(".money span.r::text").extract_first()
            item['money_spans'] = ''.join(event.css(".money span::text").extract())
            item['group_nolink'] = event.css(".group span::text").extract()
            item['group_text'] = event.css(".group a::text").extract()
            item['group_href'] = event.css(".group a::attr(href)").extract()
            item['view_url'] = self.format_url(response, event.css(".view a::attr(href)").extract_first())
            yield item
        for newp in response.css(".page-list a::attr(href)").extract():
            yield response.follow(newp, callback=self.parse_inv)

    def parse_ipo(self, response):
        for event in response.xpath('//ul[@id="ipo-list"]/li'):
            item = IPOItem()
            item['date_str'] = event.css("span.time::text").extract_first()
            if not item['date_str']:
                yield item

            item['money_spans'] = ''.join(event.css(".money span::text").extract())
            item['company'], item['company_url'] = self.get_company_and_url(response, event, 'company')
            item['industry'], item['industry_url'] = self.get_company_and_url(response, event, 'industry')
            item['place'], item['place_url'] = self.get_company_and_url(response, event, 'place')

            item['view_url'] = self.format_url(response, event.css(".view a::attr(href)").extract_first())
            yield item
        for newp in response.css(".page-list a::attr(href)").extract():
            yield response.follow(newp, callback=self.parse_ipo)

    def parse_ma(self, response):
        for event in response.xpath('//ul[@id="ma-list"]/li'):
            item = MAItem()
            item['date_str'] = event.css("span.time::text").extract_first()
            if not item['date_str']:
                yield item

            item['money_spans'] = ''.join(event.css(".money span::text").extract())
            item['company'], item['company_url'] = self.get_company_and_url(response, event, 'company')
            item['industry'], item['industry_url'] = self.get_company_and_url(response, event, 'industry')
            item['company2'], item['company2_url'] = self.get_company_and_url(response, event, 'company2')

            item['view_url'] = self.format_url(response, event.css(".view a::attr(href)").extract_first())
            yield item
        for newp in response.css(".page-list a::attr(href)").extract():
            yield response.follow(newp, callback=self.parse_ma)

    def parse_pe(self, response):
        for event in response.xpath('//ul[@id="pe-list"]/li'):
            item = PEItem()
            item['date_str'] = event.css("span.time::text").extract_first()
            if not item['date_str']:
                yield item

            item['fund'], item['fund_url'] = self.get_company_and_url(response, event, 'fund')
            item['group'], item['group_url'] = self.get_company_and_url(response, event, 'group')

            item['money_spans'] = ''.join(event.css(".money span::text").extract())
            item['view_url'] = self.format_url(response, event.css(".view a::attr(href)").extract_first())
            yield item
        for newp in response.css(".page-list a::attr(href)").extract():
            yield response.follow(newp, callback=self.parse_pe)
