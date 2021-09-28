
import AccountManager 
import websocket, json
from Config import *
from threading import *
from binance.enums import *
import TelegramBot
import DatabaseManager 
from Tools import *
BASESOCKET = "wss://stream.binance.com:9443/ws/"  
SOCKET=""


def on_open(ws):
    print('opened connection')



def on_close(ws):
  print('closed connection')
 


def need_to_buy_check(coin,time,currvalue):   
  print("Checking if need to buy -\n Coin - {coin}\tcurrent value - {currvalue}$\tTimestamp -{time} ")
  ## Write Your buy order logic here, I recommend you to use the AccountnManager and DatabaseManager Classes to     make the interface with Binance and with your database easier.
   


def need_to_sell_check(coin,value,msgtime,purchasevalue,purchasetime): 
  print("Checking if need to sell Coin - {coin}\tPurchase value - {purchasevalue}\tPurchase time - {time}")              
  ## Write your sell order logic here,  I recommend you to use the AccountnManager and DatabaseManager Classes to     make the interface with Binance and with your database easier.
  


def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    value = candle['c']
    cointype= candle['s']
    time = candle['t']
    highest=candle['h']
    lowest=candle['l']
    dbm=DatabaseManager.DatabaseManager
    currtrading=dbm.is_trading(cointype)
    #print(f"UPDATE: coin:{cointype}\ttime:{date}\t value={value}")
    if is_candle_closed: #candle closed scenario
      dbm.save_candle(cointype,value,time,highest,lowest)              
    elif currtrading:
      need_to_sell_check(cointype,time,value,currtrading[1],currtrading[2])
    else:   
      need_to_buy_check(cointype,value,time) 




def start_listen():                 
    ws1 = websocket.WebSocketApp(SOCKET,on_open=on_open, on_close=on_close, on_message=on_message)
    ws1.run_forever()


def get_socket_value(coin,interval): 
    SOCKET=""
    SOCKET +=  BASESOCKET + coin + "usdt@kline_" + interval
    return SOCKET

    

for coin in coins:
  t=Thread(target=start_listen)
  SOCKET=get_socket_value(coin,"1d")
  t.start()
  




 