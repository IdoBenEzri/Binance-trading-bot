# Binance-Trading-Bot-Documentation 

## About
Binance is a crypto coins live market, using Binance API 
and the Python language, I developed a live trading bot that trade automatically 
and update the user whenever a given trading scenario occurred using 
messages in a Telegram group,

__how it works:__
using DatabaseManager, which is a class that I wrote to take care of the bot-database interface, and using AccountManager, which is a Class that I wrote to take care of the 
bot-Binance interface, the bot constantly scanning crypto coins prices using websockets and use his database saved data to take a decision by its own in real-time using given (yours) trading algoritm.
You can find the DatabaseManager and the AccountManager classes more extendedtly later in this document.



## Enviroement Setup
1. Install PosgreSQL and create a server and a database.
2. Libraries to install using pip:
  -   pip install python-binance (to integrate with Binance as client)
  -   pip install psycopg2 (to integrate with a PosgreSQL Database)
  -   pip install python-telegram-bot (to update the user in real-time using Telegram chat)
  

## User Configuration
Before we start trading, first the bot need to be configured to one's Binance account, TelegramBot and PosgreSQL database.
In order to make the configuration a little bit easier, you can use "config.py", the configuration file in this repository which contains all the information that need to be configured (TelegramBot bot token, Binance API KEY and API SECRET, etc.).


## Database - Explanation & Building
Explanation:

You can work with your own database and not use DatabaseManager.py in this repository, but I decided to provide a DatabaseManager Class that help you evoid much of the work, however this class is currently configured to work with my own platform of database, so here is an explaination about my database:

My default database contains a table for every coin that you wish to trade (edit your coin list in config.py), 
trading with USDT (crypto coin that represant USD).

Every table contains history of a certain coin trading candlesticks, for every row in the table (that represent a certain candlestick)  we will save the close price, close time, highest price in the candlestick and lowest price in the candlestick.
Two more important tables in this database are  the "orders" table and the "currently trading" table:
- the order table:
  the orders table is a table that contain information about the bot orders - buying and selling, 
  for every row in this table (that represant an order) we will save the order serial number (auto generated), name of the coin, buying price, buying time, sell price and 
  sell time (for buying order, sell price and sell time are set to 0 by default).
  
- the currently trading table:
  this table contains all the coins we are currently trading (those we baught but didn't sell yet), 
  for every row in this table we will save the coin name, the buying price and   the buying time. 

How to build default database:

Simply run DatabaseBuilder.py 

__NOTICE__ - you should to run  DatabaseBuilder.py only a after you complete "Invorement Setup" and "User Configuration".

## Class DataBaseManager - Helper for handling the bot-Database interface:

__Methods:__

- __init__( self ) - Builder, initiate a new DatabaseManager, method open a connection with your PosgreSQL database.

- build_database ( self ) - Method builds the defauld database.

- save_buy( self, coin, value,time ) -

  Arguments - string "coin" set to coin name written in this format "BTCUSDT", float "value" represents the buying value, 
  int "time" represent a timestamp set to the candle starting time.
  
  Method save a new buy order in the "orders" table (with sell time and sell value sets to 0 by default) and in the currently trading table.
  
- save_sell(self, coin, buy_value, buy_time, sell_value, sell_time)

  Arguments- string "coin" set to coin name written in this format "BTCUSDT", int "buy_value", int "buy_time", int "sell_value", int "sell_time".
  
  Method save a new sell order in the "orders table" and remove the order from the currently trading table.
  
- save_candle(self, coin, close_value, close_time, highest, lowest)

  Arguments - string "coin" set to coin name written in this format "BTCUSDT", floats "close_value","higest","lowest" which rerepresents the candlestick close/highest/lowest       price, int "close_time" rerepresent the candle close time.
  
  Method save a new candlestick in the database.
  
- get_last_candle(self, coin):

  Arguments - string "coin" set to coin name written in this format "BTCUSDT".
  
  Method returns the time of  last candle  saved in the database, if cannot find any candle, method returns 0 
  
- print_last_candles(self):
 
  Method print the last candle for every coin in the coin list at config.py.
  
- print_orders(self):

  Method prints all the completed orders in the orders table (which are completed trades), indicating the coin name, the total hours we've been in this trade, the buying time,     the buying price, the sell time and the sell price, representing good trades first (those trades which we sold in a higher price than the price we buaght).
  
- get_highest(self, coin, start, end):

  Arguments - string coin set to a coin name written in this format "BTCUSDT", int start,end rerepresents timstamps to your starting time and ending time.
  
  Method returns the highest price the coin ever was between the given start and end times.
  
- get_lowest (self, coin, start, end):

  Method is same as get_highest, just returns the lowest price.
  
- is_trading (self, coin):

  Arguments - string "coin" set to a coin name written in this format "BTCUSDT".
  
  Methods checks if we trade certain coin right now, if we are - method returns the trade information, returns None otherwise.
  
- delete_history(self, coin, start=None) 

  Arguments -  string "coin" set to a coin name written in this format "BTCUSDT", *optional* - int "start" represent a timestamp of the earliest candlestick to delete.
  
  Method deletes a certain coin candlesticks history.
  
- fill_history(self,coin,start):

  Arguments - string "coin" set to a coin name written in this format "BTCUSDT", *optional* - int "start" represent a timestamp of the earliest candlestick to add,defauld to 300   days otherwise.
  
  Method fill candlesticks history for a certain coin.
  
- repair_history(self,start):

  Method deletes all candlesticks history and re-fill it for any coin in "coins" list (via config.py).
  
- __del__(self):
- 
  Class destructur, close the connection for the DatabaseManager.  
  
  
## Class AccountManager - helper for handling the bot-Binance interface: 

  __Methods:__

-  __init__( self ) - Builder, initiate a new AccountManager.

- order(self,side,quantity,symbol):

  Arguments - string "side" prepresent the side of the order, int quantity represent the quantity of coins to relate, string "symbol" set to a coin name written in this format "BTCUSDT".
  
 Method send a market order request to binance to buy/sell given quantity of a given coin.
 
- get_coin_balance(self,coin):

  Arguments - string "coin" set to a coin name written in this format "BTCUSDT" or to "USDT" 
  
  Method returns the current free balance of a given crypto coin there is in the user Binance account.
  
- get_quantity(self,price):

  Arguments - float "price" set to a coin certain price(trading with USDT).
  
  Method returns the max quantity the user can buy of a coin.
  
  (taking caution step of leaving 4 dollars in the USDT balance to evoid over-quantity misscalculations.)
  
- sell_coin(self,symbol): 

  Arguments - string "symbol" set to a coin name written in this format "BTCUSDT" or to "USDT"
  
  Method try to sell all user balance in a given coin, return True if succeded, False otherwise. 
  
- buy_coin(self,symbol,price):

  Arguments - string "symbol" set to a coin name written in this format "BTCUSDT" , float "price" float "price" set to a coin certain price(trading with USDT).
  
  Method try to buy the maximum quantity possible considering user current USDT balance, return True if succeded, False otherwise. 
  
## Other helper methods - Statistic.py
__Methods:__
- get_win_ratio(coin)

  Arguments -  string "coin" set to a coin name written in this format "BTCUSDT". 
  
  Method returns  a list of two integers represeting the wins and the loses trades the bot has with the given coin.
  (win/lose is depended on either we sold in a better price then we baught or not)
   
- is_good_ratio(coin,ratio):
  
  Arguments - string "coin" set to a coin name written in this format "BTCUSDT", int "ratio" set to the min ratio to consider a win/lose ratio to be good 
  (ratio answer the inequality  loses*ratio<=wins)
  
  Method return 1 if a coin has good win/lose ratio, 0 if not. Good ratio is set to be the given argument "ratio".
  
## Other helper methods - Tools.py
__Methods:__
- get_date(timestamp):

  Arguments - timestamp
  
  Method returns a String contains the excat date of the given argument "timestamp".
## TelegramBot.py 
 __Methods:__
  
  telegram_bot_sendtesxt(bot_message,chat_id):
  
  Arguments - String "bot_message", int "chat_id" present the telegram chat id.
  
  Method send a given telegram message to a given chat id. 
  
## Bot.py - Main file
 __Methods:__ 
- on_open(ws):
 
 Arguments - Websocket ws 
 
 Method print that websocket connection opened.
 
- on_close(ws):
- 
  Arguments - Websocket ws 
  
  Method print that websocket connection closed.
  
- on_message(ws, message):  
  
  Arguments - Websocket "ws", webseocket recieved message "message" 
    
  Method recieves any update about a coin price change directly from Binance, saving whenever a candlestick closed in the user PosgreSQL database, 
  checks if we currently trading the coin we recieved update on, if we are - method activate the method - "need_to_sell_check",
  else method activate the method  "need_to_buy_check".
 
-  need_to_buy_check(coin,time,currvalue):

    Arguments - string "coin" set to a coin name written in this format "BTCUSDT",
    int "time" which is a timestamp, float "currvalue" presents the current price of the given     coin   in USDT.
  
    Method recieving message about a coin price change from method "on_message", and applying User buying algoritm.  
    __This function is not fullfilled, I left it open for any User to develop his own buying algoritm, I recommend you to use the AccountnManager and DatabaseManager Classes to     make the interface with Binance and with your database easier.__
  
- need_to_sell_check(coin,value,msgtime,purchasevalue,purchasetime):

  Arguments - string "coin" set to a coin name written in this format "BTCUSDT", float "value" presents the current price of the given coin  in USDT. int "msgtime" sets to the     current candlestick open time, float "purchasevalue" presents the buying price of the current trade, int "purchasetime" presentst the buying time.
  
  Method recieving message about a coin price change from method "on_message", and applying User sellig algoritm (activated only for coins the user currently trading).
 
- start_listen():
   Method use the module websocket, creates a websocket and runs it.
   
-  get_socket_value(coin,interval): 
    
   Arguments - string coin string "coin" set to a coin name written in this format "btc", int "interval" represent candlestick time interval.
   
   Method returns a string present the full url request to open binance websocket for the given coin and given interval.
   
   __Finally - after applying your buying/selling algoritms   you can enjoy your own  Binance trading bot! simply run bot.py, I recommend to use the "repair_history" method (under DatabaseManager Class)   from time to time.__
   
