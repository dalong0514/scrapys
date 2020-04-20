# -*- coding: utf-8 -*-
import scrapy
from readreview.items import ReadreviewItem
import re

class ReviewSpider(scrapy.Spider):
    name = 'review'
    start_urls = ['https://book.douban.com/subject/1230036/reviews']

    def parse(self, response):
        urls = response.xpath('//div[@class="main-bd"]/h2/a')

        for url in urls:
            yield response.follow(url, callback=self.parse_review_pages)

        # the next page
        # the reason for using lists is a puzzle
        next_url = response.xpath('//span[@class="next"]/a')
        for url in next_url:
            yield response.follow(url, callback=self.parse)
        # next_page = response.xpath('//span[@class="next"]/a')
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_review_pages(self, response):
        item = ReadreviewItem()

        item['title'] = response.xpath('//div[@class="article"]/h1/span/text()').extract()
        item['author'] = response.xpath('//header[@class="main-hd"]/a/span/text()').extract()
        item['date'] = response.xpath('//span[@class="main-meta"]/text()').extract()
        item['url'] = ['['+response.xpath('//div[@class="article"]/h1/span/text()').extract()[0]+']('+response.xpath('//meta[@property="og:url"]/@content').extract()[0]+')']
        item['collect'] = int(re.findall(r"\d+\.?\d*",response.xpath('//button[contains(@class,"useful")]/text()').extract()[0])[0])
        item['readview'] = response.xpath('//div[@class="review-content clearfix"]//text()').extract()
        
        yield item
