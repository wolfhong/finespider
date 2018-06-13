# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class WithplashSpider(scrapy.Spider):
    name = 'withplash'
    allowed_domains = ['www.ishuhui.com']
    start_urls = ['http://www.ishuhui.com/cartoon/book/1']
    custom_settings = {
        'SPLASH_URL': 'http://127.0.0.1:8050',
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'SPLASH_COOKIES_DEBUG': False,  # True if debug
        'SPLASH_LOG_400': True,
        'ROBOTSTXT_OBEY': False,  # robots obey
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def format_url(self, response, url):
        return response.urljoin(url) if url else url

    def parse(self, response):
        for part in response.css('ul.c-post-list li'):
            number = part.css('a.post span.number::text').extract_first()
            title = part.css('a.post::attr(title)').extract_first()
            href = self.format_url(response, part.css('a.post::attr(href)').extract_first())
            if href and number and title:  # style like http://www.ishuhui.com/cartoon/book/1
                yield {'href': href, 'number': number, 'title': title}
            else:  # another style like http://www.ishuhui.com/cartoon/book/25
                number = part.css('div.post-arr span.number::text').extract_first() or ''
                for spanpart in part.css('div.post-arr a'):
                    href = self.format_url(response, spanpart.css('a::attr(href)').extract_first())
                    title = spanpart.css('a::text').extract_first() or ''
                    title = number + title
                    yield {'href': href, 'number': number, 'title': title}
