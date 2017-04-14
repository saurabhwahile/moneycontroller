# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Stock(scrapy.Item):
  name = scrapy.item.Field()
  timestamp = scrapy.item.Field(serializer=str)