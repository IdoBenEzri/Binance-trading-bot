# Binance-Trading-Bot-Documentation
Binance trading bot - Skeleton of my trading bot 


# About
Binance is a crypto coins live market, using Binance API 
and the Python language, I developed a live trading bot that trade automatically 
and update the owner whenever a given trading scenario occurred using 
messages in a Telegram group,

how it works:
using DatabaseManager, which is a class that I wrote to take care of the bot-database interface, and using AccountManager, which is a Class that I wrote to take care of the 
bot-Binance interface, the bot constantly scanning crypto coins prices using websockets and use his database saved data to take a decision by its own in real-time using given (yours) trading algoritm.
Under "Classes" in this document you can find the DatabaseManager and the Account manager classes more extendedtly.


# Invorement Setup
1. Install PosgreSQL and create a server and a database.

2. Libraries to install using pip:
- pip install python-binance (to integrate with Binance as client)
- pip install psycopg2 (to integrate with a PosgreSQL Database)
- pip install python-telegram-bot (to update the owner in real-time using Telegram chat)
  

# User Configuration
Before we start trading, first the bot need to be configured to one's Binance account, TelegramBot and PosgreSQL database.
In order to make the configuration a little bit easier, you can use "config.py", the configuration file in this repository which contains all the information that need to be configured (TelegramBot bot token, Binance API KEY and API SECRET, etc.).


# Database - Explanation & Building
Explanation:

You can work with your own database and not use DatabaseManager.py in this repository, but I decided to provide a DatabaseManager Class that help you evoid much of the work, however this class is currently configured to work with my own platform of database, so here is an explaination about my database:

My default database contains a table for every coin that you wish to trade (edit your coin list in config.py), trading with USDT (crypto coin that represant USD).
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

NOTICE - you should to run  DatabaseBuilder.py only a after you complete "Invorement Setup" and "User Configuration".


# Classes
DataBaseManager - class to help handling the bot-database interface.

Methods:
- init(self) - Builder, initiate a new DatabaseManager, method open a connection with your PosgreSQL database.
- build_database(self) - Method builds the defauld database.
- save_buy(self,coin,value,time) -

  Arguments - string "coin" set to coin name presented in this format "BTCUSDT", float "value" presents the buying value, 
  int "time" present a timestamp set to the candle starting time.
  
  Method save a new buy order in the "orders" table (with sell time and sell value sets to 0 by default) and in the currently trading table.
  
- save_sell(self,coin,buy_value,buy_time,sell_value,sell_time)
  Arguments- string "coin" set to coin name presented in this format "BTCUSDT", int "buy_value", int "buy_time", "int sell_value", int "sell_time".
  
  Method save a new sell order in the "orders table" and remove the order from the currently trading table.
  
- save_candle(self,coin,close_value,close_time,highest,lowest)
  Arguments - string coinset to coin name presented in this format "BTCUSDT", floats close_value,higest,lowest which represents the candlestick close/highest/lowest price, int     close_time represent the candle close time.
  
  Method save a new candlestick in the database.
  
- get_last_candle(self,coin):
  Arguments - string "coin" set to coin name presented in this format "BTCUSDT".
  
  Method returns the time of  last candle  saved in the database, if cannot find any candle, method returns 0 
  
- print_last_candles(self):
 
  Method print the last candle for every coin in the coin list at config.py.
- print_orders(self):

  Method prints all the completed orders in the orders table (which are completed trades), indicating the coin name, the total hours we've been in this trade, the buying time,     the buying price, the sell time and the sell price, presenting good trades first (those trades which we sold in a higher price than the price we buaght).
-get_highest(self,coin,start,end):
  Arguments - string coin set to coin name presented in this format "BTCUSDT", int start,end represents timstamps to your starting time and ending time.
  Method returns the highest price the coin ever was between the given start and end times.
-get_lowest(self,coin,start,end):
  Method is same as get_highest, just returns the lowest price.
  
