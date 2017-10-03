# -*- coding: utf-8 -*-
import datetime
import re
import codecs
import scrapy

from data_scraper.parsers.MCStock import parse as parse_stock, parse_comments

from data_scraper.definitions import *

class MCStock(scrapy.Spider):
  name = "MCStock"
  comments_url = "http://mmb.moneycontrol.com/index.php?q=topic/ajax_call&section=get_messages&is_topic_page=1&offset={offset}&lmid=&isp=0&gmt=tp_lm&tid={stock_id}&pgno={page_no}"
  comments_stock_id = ""

  def __init__(self, stock_url='', *args, **kwargs):
    super(MCStock, self).__init__(*args, **kwargs)
    self.start_url = stock_url
    self.stock = None

  def start_requests(self):
    yield scrapy.Request(url=self.start_url, callback=self.parse)

  def parse(self, response):
    stock = parse_stock(response)
    self.stock = stock
    self.comments_stock_id = re.findall("\d+$", stock['comments'])[0]

    page_no = 1
    for offset in range(0, 100, 10):
      yield scrapy.Request(
        url=self.comments_url.format(stock_id=self.comments_stock_id, offset=offset, page_no=page_no), 
        callback=self.parse_comments
      )
      page_no+=1

    yield stock

  def parse_comments(self, response):
    comments = parse_comments(response.body)
    comments['stock'] = self.stock['id']
    comments['url'] = response.url
    yield comments