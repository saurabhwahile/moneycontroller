import datetime
import re
from data_scraper.definitions import *
from data_scraper.items import Stock


def parse(response):
  identifiers = re.sub('<[A-Za-z/][^>]*>', '', response.xpath('//*[@id="nChrtPrc"]/div[4]/div[1]').extract()[0])

  #get bse and nse ids
  try:
    nse = identifiers.split('|')[1].strip().split(' ')[1] 
    nse_ltp = float(response.xpath('//*[@id="Nse_Prc_tick"]/strong/text()').extract()[0])
    nse_vol = int(response.xpath('//*[@id="nse_volume"]/strong/text()').extract()[0].replace(',',''))
  except:
    nse = None
    nse_ltp = None
    nse_vol = None
  try:
    bse = identifiers.split('|')[0].strip().split(' ')[1]
    bse_ltp = float(response.xpath('//*[@id="Bse_Prc_tick"]/strong/text()').extract()[0])
    bse_vol = int(response.xpath('//*[@id="bse_volume"]/strong/text()').extract()[0].replace(',',''))
  except:
    bse = None
    bse_ltp = None
    bse_vol = None

  return {
    "name": response.xpath('//*[@id="nChrtPrc"]/div[3]/h1/text()').extract()[0],
    "nse": nse,
    "nse_ltp": nse_ltp,
    "nse_vol": nse_vol,
    "bse": bse,
    "bse_ltp": bse_ltp,
    "bse_vol": bse_vol,
    "sector": identifiers.split('|')[3].strip().replace('&amp', '&'),
    "market_cap": float(response.xpath('//*[@id="mktdet_2"]/div[1]/div[1]/div[2]/text()').extract()[0].replace(',','')),
    "pe": float(response.xpath('//*[@id="mktdet_2"]/div[1]/div[2]/div[2]/text()').extract()[0].replace('-', '0')),
    "book_value": float(response.xpath('//*[@id="mktdet_1"]/div[1]/div[3]/div[2]/text()').extract()[0]),
    "dividend": float(response.xpath('//*[@id="mktdet_2"]/div[1]/div[4]/div[2]/text()').extract()[0].replace('%', '').replace('-', '0')),
    "eps": float(response.xpath('//*[@id="mktdet_2"]/div[2]/div[1]/div[2]/text()').extract()[0].replace('-', '0')),
    "pc": float(response.xpath('//*[@id="mktdet_2"]/div[2]/div[2]/div[2]/text()').extract()[0].replace('-', '0')),
    "fv": float(response.xpath('//*[@id="mktdet_2"]/div[2]/div[5]/div[2]/text()').extract()[0]),
    "deliverables": float(response.xpath('//*[@id="tt07"]/a/text()').extract()[0]),
    "url": response.url,
    "type": STOCK,
    "timestamp": datetime.datetime.now().isoformat()
  }