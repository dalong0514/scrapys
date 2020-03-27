# -*- coding: utf-8 -*-
import scrapy
from stackof.items import StackofItem
import re

class BasicSpider(scrapy.Spider):
    name = 'basic'
    # allowed_domains = ['https://stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/tagged/python?tab=votes&pagesize=30']

    def parse(self, response):
        urls = response.xpath('//div[@class="summary"]/h3/a')
        for url in urls:
            yield response.follow(url, callback=self.parse_review_pages)

        # the next page
        # the reason for using lists is a puzzle
        next_url = response.xpath('//a[@rel="next"]')
        for url in next_url:
            yield response.follow(url, callback=self.parse)
        # next_page = response.xpath('//span[@class="next"]/a')
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_review_pages(self, response):
        item = StackofItem()

        item['title'] = response.xpath('//h1[@itemprop="name"]/a/text()').extract()[0]
        item['author'] = response.xpath('//div[@itemprop="author"]/a/text()').extract()[0]
        item['date'] = response.xpath('//div[@class="user-action-time"]/span/@title').extract()[0]
        item['question'] = ''.join(response.xpath('//div[@class="question"]//div[@class="post-text"]/p//text()').extract())
        item['url'] = '['+response.xpath('//h1[@itemprop="name"]/a/text()').extract()[0]+']('+'https://stackoverflow.com'+response.xpath('//h1[@itemprop="name"]/a/@href').extract()[0]+')'
        # item['url'] = 'https://stackoverflow.com' + response.xpath('//h1[@itemprop="name"]/a/@href').extract()[0]
        item['vote'] = int(response.xpath('//div[@itemprop="upvoteCount"]/text()').extract()[0])
        item['content'] = ''.join(response.xpath('//div[@class="post-text"]/p//text()').extract())
        
        yield item
