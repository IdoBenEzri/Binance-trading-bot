import requests
from Config import *
def telegram_bot_sendtext(bot_message,chat_id):
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    response = requests.post(send_text)
    return response.json()









   