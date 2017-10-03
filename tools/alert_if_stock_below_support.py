from googlefinance import getQuotes
import winsound
import time
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("stock", help="A google supported stock name. Example, NASDAQ:AAPL", type=str)
parser.add_argument("support", help="beep when below this price", type=float)
args = parser.parse_args()

stock = args.stock
support = float(args.support)

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

while True:
  s = getQuotes(stock)
  ltp = float(s[0]['LastTradePrice'])
  print(ltp)
  if ltp - support < 0:
    winsound.Beep(int(37+(sigmoid(-1*(ltp-support))-0.5)*32767), 1000)
  time.sleep(60)