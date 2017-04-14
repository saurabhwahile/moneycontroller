# -*- coding: utf-8 -*-
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

from scrapy.http.request import Request

from data_scraper.definitions import *

class MCLatestNews(CrawlSpider):
  name = "MCLatestNews"
  allowed_domains = ["moneycontrol.com"]
  start_urls = ['http://www.moneycontrol.com/news/news-all.html']
  rules = [
    Rule(LinkExtractor(allow=['/news/news-all.html/page-\d/']),
      callback='parse_news_index',
      follow=True)
  ]

  def parse_news_index(self, response):
    for li in response.xpath('//*[@id="cagetory"]/li'):
      yield Request(url=li.xpath('a/@href').extract()[0], callback=self.parse_news)

  def parse_news(self, response):
    yield {
      "text": ''.join(response.xpath('//*[@id="article-main"]/p/text()').extract()),
      "type": NEWS,
      "timestamp": datetime.datetime.now().isoformat(),
    }