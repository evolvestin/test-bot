import gspread
import os
import _thread
import telebot
import subprocess
import sys
from telegraph import upload
from time import sleep
from datetime import datetime
os.environ["DEBUSSY"] = 'l'
stamp = datetime.now().timestamp()


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


while True:
    os.system("echo Hello from the other side!")
    install('e-objects>=2.10.1')
    print('Ушло на установку одного модуля', datetime.now().timestamp() - stamp, 'секунд')
    sleep(1000)
