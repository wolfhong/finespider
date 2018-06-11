# -*- coding: utf-8 -*-
import sys
import scrapy
# from scrapy.http.headers import Headers

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode


RENDER_HTML_URL = "http://127.0.0.1:8050/render.html"


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['www.ishuhui.com']
    start_urls = ['http://www.ishuhui.com/cartoon/book/1']

    def start_requests(self):
        for url in self.start_urls:
            params = {"url": url, "wait": 0.5}
            url = '%s?%s' % (RENDER_HTML_URL, urlencode(params))
            print('real-url: ', url)
            # headers = Headers({'Content-Type': 'application/json'})
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for part in response.css('ul.c-post-list li'):
            href = part.css('a.post::attr(href)').extract_first()
            number = part.css('a.post span.number::text').extract_first()
            title = part.css('a.post span::text')[1].extract()
            if href:
                href = response.urljoin(href)
            yield {'href': href, 'number': number, 'title': title}
