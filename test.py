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
test = ['emoji==1.7.0', 'Pillow>=9.1.0', 'gspread>=3.6.0', 'requests>=2.20.0', 'telegraph==1.4.1', 'GitPython==3.1.17']


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


while True:
    os.system("echo Hello from the other side!")
    for i in test:
        install(i)
    print('Ушло на установку 6 модулей', datetime.now().timestamp() - stamp, 'секунд')
    sleep(1000)
