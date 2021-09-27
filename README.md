# Binance-Trading-Bot 
Binance trading bot - Skeleton of my trading bot 

# About
Binance is a crypto coins live market, using Binance API 
and the Python language, I developed a live trading bot that trade automatically 
and update the owner whenever a given trading scenario occurred using 
messages in a Telegram group,

# Invorement Setup
1.Install PosgreSQL and create a server and a database.
2.Lbraries to install using pip:
  - pip install python-binance (to integrate with Binance as client)
  - pip install psycopg2 (to integrate with a PosgreSQL Database)
  - pip install python-telegram-bot (to Update the owner inreal time using Telegram chat)
  

# User Configuration
The bot has a simple configuration, all one need to do is to edit "config.py" file update to his Binanace User information, Database information and Telegram information (Bot and group information)
