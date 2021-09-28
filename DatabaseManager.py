from Config import *
import psycopg2
import psycopg2.extras
from binance.client import Client
from binance.enums import *
from Tools import *


class DataBaseManager():
      
  def __init__(self):
    self.conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)
    self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     
  def save_candle(self,coin,value,time,highest,lowest):
    self.cur.execute("INSERT INTO "+coin+" VALUES(%s,%s,%s,%s)",(value,time,highest,lowest))  
    self.conn.commit() 

  def get_last_candle(self,coin):
    self.cur.execute("SELECT max(msgtime) FROM "+coin+"") 
    last_candle=self.cur.fetchone()
    if not last_candle or not last_candle[0]:
      return 0
    return last_candle[0]

  def print_last_candles(self):          
    for coin in coins:
      name=str(coin).upper()+"USDT"     
      last_candle=self.get_last_candle(name)
      d=get_date(last_candle)
      print(f"Coin - {coin} \t{d}\t{last_candle}")


  def print_orders(self):
      self.cur.execute("SELECT * FROM orders as p WHERE p.purchasevalue<p.sellvalue AND p.sellvalue>0")
      goodtrades=self.cur.fetchall()
      for row in goodtrades:
          pvalue =row[2]
          ptime=get_date(row[3])
          svalue=row[4]
          stime=get_date(row[5])
          cname=row[1]
          marks="**********************************"
          duration=(float(row[5])-float(row[3]))/(60*minute)
          print(f"Good trade - Coin name: {cname}\tTotal hours in trade - {duration}\nPurchase Time - {ptime}\tPurchase Value - {pvalue}\nSell Time - {stime}\tSell Value - {svalue} \n{marks}")
      self.cur.execute("SELECT * FROM orders WHERE   purchasevalue>sellvalue and sellvalue>0")
      badtrades=self.cur.fetchall()
      for row in badtrades:
          pvalue =row[2]
          ptime=get_date(row[3])
          svalue=row[4]
          stime=get_date(row[5])
          cname=row[1]
          duration=(float(row[5])-float(row[3]))/(60*minute)
          print(f"Bad trade - Coin name: {cname},\tTotal hours in trade:{duration}\n{marks}")


  def get_highest(self,coin,start,end):
      self.cur.execute("SELECT max(highest) FROM "+coin+" WHERE msgtime>=%s and msgtime<=%s",(start,end))
      row=self.cur.fetchone()
      if row:
        return row[0]
      return 0


  def get_lowest(self,coin,start,end): 
      self.cur.execute("SELECT min(lowest) FROM "+coin+" WHERE  msgtime>=%s and msgtime<=%s",(start,end))
      row=self.cur.fetchone()
      if row:
          return row[0]
      return 0 




  def is_trading(self,coin):  
    self.cur.execute("SELECT * FROM currentlytrading WHERE coin LIKE %s",(coin,))
    istrade=self.cur.fetchone()
    if istrade: 
      return istrade
    return None   



  def delete_history(self,coin,start=None):
    name=str.upper(coin)+"USDT"
    if not start:
      self.cur.execute("DELETE FROM "+name+"")
      self.conn.commit()
    else:
      self.cur.execute("DELETE FROM "+name+" WHERE msgtime >%s",(start,))
      self.conn.commit() 


  def get_close_Value(self,coin,timestamp):
      self.cur.execute("SELECT value FROM "+coin+" WHERE msgtime < '%s' AND msgtime> '%s'",(timestamp+(5*minute),timestamp-(5*minute))) 
      value=self.cur.fetchone()
      if value:
          return value[0]
      return None



  def fillHistory(self,coin,start=None): 
      client = Client(API_KEY,API_SECRET)
      name=str.upper(coin)+"USDT"
      try:
          print("sending order")
          if not start:
            candles = client.get_historical_klines(symbol=name,interval=client.KLINE_INTERVAL_1DAY,start_str="300 days ago UTC",end_str=None,limit=999)
          else:
            candles = client.get_historical_klines(symbol=name,interval=client.KLINE_INTERVAL_1DAY,start_str=start,limit=999)
          for candle in candles:
                  msgtime= candle[0]
                  value=candle[4] 
                  high=candle[2]
                  low=candle[3]
                  self.cur.execute("INSERT INTO "+name+" VALUES(%s,%s,%s,%s)",(value,msgtime,high,low))
                  self.conn.commit()                
          print(f"Coin -{name} Filled! ")  
      except Exception as e:
          print("{}".format(e))
          print(f"Coin -{name}- errored.") 


  def print_last_candles(self):          
    for coin in coins:
      name=str(coin).upper()+"USDT"     
      last_candle=self.get_last_candle(name)
      d=get_date(last_candle)
      print(f"Coin - {coin} \t{d}\t{last_candle}")

  def deleteHistory(self,coin,start=None):
    name=str.upper(coin)+"USDT"
    #start=1631024100000-(2*minute)
    if not start:
      self.cur.execute("DELETE FROM "+name+"")
      self.conn.commit()
    else:
      self.cur.execute("DELETE FROM "+name+" WHERE msgtime >%s",(start,))
      self.conn.commit() 


  def RepairHistory(self):
    print("Deleting old history...")
    for coin in coins:
      self.deleteHistory(coin)
    print("Old history deleted,re-filling history:")   
    for coin in coins:
      self.fillHistory(coin)

  def  __del__(self):
    self.cur.close()
    self.conn.close()

