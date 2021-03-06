# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EquipmentItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    bigclass = scrapy.Field()
    briefinfo = scrapy.Field()
    intro = scrapy.Field()
    devicetype = scrapy.Field()
    breakdown = scrapy.Field()
