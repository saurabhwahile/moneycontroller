import datetime
import re
import json
from data_scraper.definitions import *
from data_scraper.items import Stock


def parse(response):
  identifiers = re.sub('<[A-Za-z/][^>]*>', '', response.xpath('//*[@id="nChrtPrc"]/div[4]/div[1]').extract()[0])
  stock = {}
  #get bse and nse ids
  try:
    stock["nse"] = identifiers.split('|')[1].strip().split(' ')[1] 
    stock["nse_ltp"] = float(response.xpath('//*[@id="Nse_Prc_tick"]/strong/text()').extract()[0])
    stock["nse_vol"] = int(response.xpath('//*[@id="nse_volume"]/strong/text()').extract()[0].replace(',',''))
  except:
    stock["nse"] = None
    stock["nse_ltp"] = None
    stock["nse_vol"] = None
  try:
    stock["bse"] = identifiers.split('|')[0].strip().split(' ')[1]
    stock["bse_ltp"] = float(response.xpath('//*[@id="Bse_Prc_tick"]/strong/text()').extract()[0])
    stock["bse_vol"] = int(response.xpath('//*[@id="bse_volume"]/strong/text()').extract()[0].replace(',',''))
  except:
    stock["bse"] = None
    stock["bse_ltp"] = None
    stock["bse_vol"] = None

  stock["name"] = response.xpath('//*[@id="nChrtPrc"]/div[3]/h1/text()').extract()[0]
  stock["sector"] = identifiers.split('|')[3].strip().replace('&amp', '&')
  stock["market_cap"] = float(response.xpath('//*[@id="mktdet_2"]/div[1]/div[1]/div[2]/text()').extract()[0].replace(',',''))
  stock["pe"] = float(response.xpath('//*[@id="mktdet_2"]/div[1]/div[2]/div[2]/text()').extract()[0].replace('-', '0'))
  stock["book_value"] = float(response.xpath('//*[@id="mktdet_1"]/div[1]/div[3]/div[2]/text()').extract()[0])
  try: 
    stock["dividend"] = float(response.xpath('//*[@id="mktdet_2"]/div[1]/div[4]/div[2]/text()').extract()[0].replace('%', '').replace('-', '0'))
  except: 
    stock["dividend"] = 0
  stock["eps"] = float(response.xpath('//*[@id="mktdet_2"]/div[2]/div[1]/div[2]/text()').extract()[0].replace('-', '0'))
  stock["pc"] = float(response.xpath('//*[@id="mktdet_2"]/div[2]/div[2]/div[2]/text()').extract()[0].replace('-', '0'))
  stock["fv"] = float(response.xpath('//*[@id="mktdet_2"]/div[2]/div[5]/div[2]/text()').extract()[0])
  try: 
    stock["deliverables"] = float(response.xpath('//*[@id="tt07"]/a/text()').extract()[0]) 
  except: 
    stock["deliverables"] = 0
  stock["url"] = response.url
  stock["comments"] = response.xpath('//*[@id="slider"]/dt[4]/a/@href').extract()[0]
  stock["timestamp"] = datetime.datetime.now().isoformat()
  stock["id"] = stock["nse"] if stock["nse"] not in ['', None, ' '] else stock["bse"]
  stock["type"] = STOCK

  return stock

def parse_comments(response):
  comments_dict = json.loads(response.decode('utf-8', errors='replace'))
  comments = []
  for comment in comments_dict:
    comments.append(comment['full_message'])
  return {
    COMMENTS: comments,
    "type": COMMENTS,
    "timestamp": datetime.datetime.now().isoformat()
    "sanitized": False
  }