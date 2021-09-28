from Config import *
from binance.client import Client
from binance.enums import *
from Tools import *
import math


class AccountManager(): 
  def __init__(self):
      client = Client(API_KEY,API_SECRET)
        

  def order(self,side, quantity, symbol):
    try:
      print("sending order")
      order = self.client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_MARKET, quantity=quantity)
      print(order)
    except Exception as e:
      print("an exception occured - {}".format(e))
      return False
    return True


  def get_coin_balance(self,coin):
      if str.upper(coin)!="USDT":
        index=str.upper(coin).find("USDT")
        coin=coin[:index]
      balance =self.client.get_asset_balance(coin)
      return balance['free']   


  def get_quantity(self,price):
    balance=self.get_coin_balance("usdt")
    quantity=math.floor((float(balance)-4)/float(price))
    return quantity
    

  def sell_coin(self,symbol):
    balance=math.floor(float(self.get_coin_balance(symbol)))
    print(f"!! selling coin - {symbol} our balance - {balance} ")    
    flag =self.order(side=SIDE_SELL,quantity=balance,symbol=symbol)
    print(f"flag ={flag}")
    return flag


  def buy_coin(self,symbol,price):    
    balance=self.get_coin_balance("usdt")
    quantity =self.get_quantity(price)
    print(f"!! buying coin - {symbol} our usdt balance - {balance}\t quantity to buy:{quantity} ")
    flag= self.order(SIDE_BUY,quantity,symbol,ORDER_TYPE_MARKET)
    print(f"flag ={flag}")
    return flag 


