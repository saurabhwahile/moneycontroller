import datetime
import scrapy
import logging

from  scrapy.http.request import Request

from w3lib.html import remove_tags


from data_scraper.parsers.MCStock import parse as parse_stock
from data_scraper.definitions import *

class testspider(scrapy.Spider):
    name = 'testspider'

    start_urls = ['http://www.moneycontrol.com/news/business/companies/startup-woes-stayzilla-ceo-to-remain-behind-bars-court-denies-bail-2245775.html']

    def parse(self, response):
        d = response.xpath('//*[@id="article-main"]')
        for a in d.xpath('p'):
            yield {
                "a": a.extract(),
                "type": NEWS
            }