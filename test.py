import gspread
import os
import _thread
import telebot
from telegraph import upload
from time import sleep
os.environ["DEBUSSY"] = 'l'

bot = telebot.TeleBot('429683355:AAF3GReDyewByK-WRLQ44xpCNKIsYg1G8X0')


def environmental_files():
    directory = os.listdir('.')
    for key in os.environ.keys():
        if (key.endswith('.json') or key.endswith('.py')) and key not in directory:
            file = open(key, 'w')
            file.write(os.environ.get(key))
            file.close()


while True:
    bot.send_document(396978030, open('xstorage1.json', 'rb'))
    bot.send_document(396978030, open('token.py', 'rb'))
    #acc = gspread.service_account('worker1.json')
    #files = acc.list_spreadsheet_files()
    #for i in files:
    #    print(i)
    sleep(1000)
