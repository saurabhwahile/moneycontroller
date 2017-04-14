# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from data_scraper.utils import get_elasticsearch_base_url
import requests
import json
import logging
from data_scraper.definitions import *

class ElasticSearchPipeline(object):
  def __init__(self):
    self.es_session = requests.Session()

  def process_item(self, item, spider):
    if(item['type']==STOCK):
      key = item['nse'] if item['nse'] not in ['', None, ' '] else item['bse']
      self.es_session.put(''.join([ES_STOCK_INDEX_URL, key]), data=json.dumps(item))
    if(item['type']==VOLUME_SHOCKERS):
      self.es_session.put(''.join([ES_MCVOLUMESHOCKER_URL, item['timestamp']]), data=json.dumps(item))
    if(item['type']==NEWS):
      self.es_session.put(''.join([ES_MCNEWS_URL, item['timestamp']]), data=json.dumps(item))
    return item