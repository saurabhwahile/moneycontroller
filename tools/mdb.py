from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
client = MongoClient('localhost', 27017)

db = client['moneycontroller']
stocks = db['stocks']

#stocks.insert({"stock": "IOC"})
#print(stocks.find({"one":1}).next())
#print(stocks.find({"stock": "IOC"}).count())
stocks.update(
  {"stock": "IOC"}, 
  {"$push", {"date":2}}
)