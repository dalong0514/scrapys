# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import requests
from collections import deque
import re, csv, json


# Change the parser below to try out different options
bs_parser = 'html.parser'
# bs_parser = 'lxml'
# bs_parser = 'lxml-xml'
# bs_parser = 'html5lib'

def get_page(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            # 如果用 big_re.text 解析失败 
            return BeautifulSoup(r.content, bs_parser)
    except Exception as e:
        print(url + ': Have not got the page')
    return None

def modify_text(line):
    """处理文字的格式"""
    
    line = line.replace(' (', '（')
    line = line.replace(') ', '）')
    line = line.replace('“', '「')
    line = line.replace('”', '」')
    line = line.replace('・', '·')
    line = line.replace('， ', '，')
    line = line.replace('。 ', '。')
    return line