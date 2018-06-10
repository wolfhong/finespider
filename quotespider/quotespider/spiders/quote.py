# -*- coding: utf-8 -*-
import scrapy
from quotespider.items import QuoteItem


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com/page/5/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            item = QuoteItem()
            item['content'] = quote.css("span.text::text").extract_first()
            item['author'] = quote.css("small.author::text").extract_first()
            about_url = quote.xpath("//span/a/@href").extract_first()
            item['about'] = response.urljoin(about_url) if about_url else ''
            item['tags'] = ','.join(quote.css("div.tags a.tag::text").extract())
            yield item
        prev_url = response.css("li.previous a::attr(href)").extract_first()
        next_url = response.css("li.next a::attr(href)").extract_first()
        if prev_url:
            yield response.follow(prev_url, callback=self.parse)
        if next_url:
            yield response.follow(next_url, callback=self.parse)
