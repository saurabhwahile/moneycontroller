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
    self.es_session.put(''.join([ES_MCINDEX_URL, item['type'], '/', item['timestamp']]), data=json.dumps(item))
    return item