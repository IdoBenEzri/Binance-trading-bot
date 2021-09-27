import time
from Config import *
import DataBaseManager

def getDate(timestamp):
    t = timestamp/1000
    humantime= time.ctime(t)
    return humantime

def getWinRatio(coin):
    dbm=DataBaseManager() 
    dbm.cur.execute("SELECT count(id) FROM orders WHERE coin LIKE %s  AND purchasevalue>sellvalue AND sellvalue>0",(coin,))
    alll=dbm.cur.fetchone()
    dbm.cur.execute("SELECT count(id) FROM orders WHERE coin LIKE %s  AND purchasevalue<sellvalue AND sellvalue>0",(coin,))  
    allw=dbm.cur.fetchone()
    wins=int(allw[0])
    loses=int(alll[0])
    del dbm
    return[wins,loses]  


def isGoodRatio(coin,ratio):
  name=str(coin)
  rates=getWinRatio(name)
  wins=rates[0]
  loses=rates[1]
  if loses*ratio<=wins:
    return 1       
  return 0

