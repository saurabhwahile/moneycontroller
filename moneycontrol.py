import sys
from google import search
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sqlite3

class CACHE:
  def __init__(self):
    self.conn = sqlite3.connect('moneycontrol_cache.db')
    self.conn.text_factory = str
    try:
      self.conn.execute(
        '''CREATE TABLE CACHE(
           ID     INTEGER PRIMARY KEY AUTOINCREMENT,
           KEY    TEXT NOT NULL UNIQUE,
           VALUE  TEXT NOT NULL
        );'''
      )
      print "Cache created successfully"
    except sqlite3.OperationalError:
      pass

  def set(self, key, value):
    key = str(key)
    value = str(value)
    try:
      self.conn.execute('INSERT INTO CACHE (KEY, VALUE) VALUES (?, ?);', (key, value))
    except sqlite3.IntegrityError:
      self.delete(key)
      self.set(key, value)
    self.conn.commit()
      
  def get(self, key):
    key = str(key)
    cursor = self.conn.execute('SELECT VALUE FROM CACHE WHERE KEY="'+key+'";')
    for row in cursor:
      return row[0]
  
  def delete(self, key):
    key = str(key)
    self.conn.execute('DELETE FROM CACHE WHERE KEY="'+key+'";')
    self.conn.commit()
    
  def clear(self):
    self.conn.execute('DROP TABLE CACHE;')
    self.conn.commit()
    
  def close(self):
    self.conn.close()
    
class HTTP:
  def __init__(self):
    self.cache = CACHE()
  
  def close(self):
    self.cache.close()
    
  def _get_fund_id(self, name):
    key = 'site:moneycontrol.com '+name
    cache_data = self.cache.get(key)
    if cache_data is None:
      for result in search(key, tld='co.in', stop=5):
        fund_id = result[result.rfind('/')+1:]
        self.cache.set(key, fund_id)
        return fund_id
    else:
      return cache_data
  
  def _get_page(self, url):
    cache_data = self.cache.get(url)
    if cache_data is None:
      page_text = requests.get(url).text.encode(sys.stdout.encoding, errors='replace')
      self.cache.set(url, page_text)
      return page_text
    else:
      return cache_data

  def get_fund_portfolio(self, name):
    fund_id = self._get_fund_id(name)
    page = BeautifulSoup(self._get_page('http://www.moneycontrol.com/india/mutualfunds/mfinfo/portfolio_holdings/'+fund_id))
    table = page.find('div', {"class": "mainCont port_hold "}).table
    headers = [header.string for header in table.tr.find_all('th')]
    headers[headers.index(None)] = 'Value'
    headers = [header.strip() for header in headers]
    results = [[cell.string for cell in row.find_all('td')] for row in table.find_all('tr')]
    results = results[1:]
    
    df = pd.DataFrame(data=results)
    df = df.rename(columns={i:col_name for i, col_name in enumerate(headers)})
    
    df['Qty'] = df['Qty'].apply(lambda x: np.float64(x.replace(',', '')))
    df['Value'] = df['Value'].apply(lambda x: np.float64(x))
    df['%'] = df['%'].apply(lambda x: float(x))
    
    return df

if __name__=='__main__':
  http = HTTP()
  df = http.get_fund_portfolio('HDFC TOP 200')
  df2 = http.get_fund_portfolio('HDFC Prudence Growth')
  print df2
  http.close()
