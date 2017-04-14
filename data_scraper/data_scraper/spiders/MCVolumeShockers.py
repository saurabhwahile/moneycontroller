import datetime
import scrapy
import logging

from  scrapy.http.request import Request

from data_scraper.parsers.MCStock import parse as parse_stock
from data_scraper.definitions import *

class MCVolumeShockers(scrapy.Spider):
    name = 'MCVolumeShockers'

    start_urls = ['http://www.moneycontrol.com/stocks/marketstats/nse_vshockers/']

    def parse(self, response):
        stocks = []
        for stock in response.xpath('//*[@id="mc_content"]/section/section/div/div[1]/div[2]/table/tbody/tr'):
            stocks.append({
                "name": stock.xpath('td/span/a/text()').extract()[0],
                "url": stock.xpath('td/span/a/@href').extract()[0],
                "avg_vol": stock.xpath('td[6]/text()').extract()[0]
            })
            yield Request(url=stock.xpath('td/span/a/@href').extract()[0], callback=self.parse_stock)
        yield {
            "stocks": stocks,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": VOLUME_SHOCKERS
        }

    def parse_stock(self, response):
        yield parse_stock(response)