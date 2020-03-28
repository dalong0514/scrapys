# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup

import equipment.spiders.utilmodule as util

class BasicSpider(scrapy.Spider):
    name = 'basic'
    start_urls = ['http://www.yzj.cc/pro-list.asp?ppid=44']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取大类的 html
        big_list = []
        for i in soup.findAll('div', class_="big_li"):
            big_list.append('http://www.yzj.cc/'+
            [link.get('href') for link in i][0])
        
        for item in big_list:
            big_soup = util.get_page(item)
            soup_strainer = big_soup.findAll('div', class_="jianjie")
            summary = [i.get_text().replace('\n', '') for i in soup_strainer]
            summary = summary[0].replace('\t', '')
            summary = summary.replace('\r', '')
            summary = summary.replace(' ', '')
            print(summary + '\n')


