# -*- coding: utf-8 -*-
import scrapy
import requests, re
from bs4 import BeautifulSoup

from equipment.items import EquipmentItem
import equipment.spiders.utilmodule as util

class BasicSpider(scrapy.Spider):
    name = 'basic'
    start_urls = ['http://www.yzj.cc/pro-list.asp?ppid=44']

    def parse(self, response):
        raw_urls = response.xpath('//div[@class="big_li"]/a/@href').extract()
        urls = []
        [urls.append('http://www.yzj.cc/'+i) for i in raw_urls]
        # [print(i) for i in urls]

        for url in urls:
            yield response.follow(url, callback=self.parse_bigli_pages)

    def parse_bigli_pages(self, response):

        raw_urls = response.xpath('//a[@class="jzimg fl"]/@href').extract()
        urls = []
        [urls.append('http://www.yzj.cc/'+i) for i in raw_urls]
        # [print(i) for i in urls]

        for url in urls:
            yield response.follow(url, callback=self.parse_detail_pages)
        
        raw_nexturls = response.xpath('//div[@class="page"]/a/@href').extract()
        nexturls = []
        [nexturls.append('http://www.yzj.cc/pro-list.asp'+i) for i in raw_nexturls]
        for url in nexturls:
            yield response.follow(url, callback=self.parse_bigli_pages)

    def parse_detail_pages(self, response):
        item = EquipmentItem()

        briefinfo = ''.join(response.xpath('//div[@class="prjianjie"]/p/text()').extract())
        item['briefinfo'] = re.sub('[\r\t]', '',briefinfo)

        item['bigclass'] = response.xpath('//div[@class="wz_title"]/text()').extract()[0]
        item['title'] = response.xpath('//h1/text()').extract()[0]

        intro = ''.join(response.xpath('(//div[@class="showpr_msg"]//h3/text()) | (//div[@class="showpr_msg"]//p/text()) | (//div[@class="showpr_msg"]//a/text()) | (//div[@class="showpr_msg"]//span/text())').extract())
        intro = re.sub('[\t\r\xa0]', '', intro)
        item['intro'] = re.sub(' ', '', intro)

        item['devicetype'] = response.xpath('(//td/div/text()) | (//td/div/div/text())').extract()

        item['breakdown'] = response.xpath('//td/p/text()').extract()

        yield item
        