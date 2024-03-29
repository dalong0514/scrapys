# -*- coding: utf-8 -*-
import scrapy
import re

from blog.items import BlogItem
import blog.spiders.utilmodule as util

class BasicSpider(scrapy.Spider):
    name = 'basic'
    start_urls = ['https://cn.vuejs.org/v2/guide/installation.html']

    def parse(self, response):
        raw_urls = response.xpath('//ul[@class="menu-root"]//a/@href').extract()
        urls = []
        [urls.append('https://cn.vuejs.org'+i) for i in raw_urls]

        for url in urls:
            yield response.follow(url, callback=self.parse_detail_pages)

    def parse_detail_pages(self, response):
        item = BlogItem()

        title = response.xpath('//h1/text()').extract()[0]
        content = ''.join(response.xpath('(//p/text()) | (//p/strong/text()) | (//h2/text()) | (//p/a/text()) | (//p/code/text()) | (//h3/text()) | (//h4/text())').extract())

        allcontent = title + '\n\n' + content
        allcontent = util.modify_text(allcontent)

        with open('/Users/Daglas/Desktop/' + title + '.md', 'w') as f:
            f.write(allcontent)

        yield item