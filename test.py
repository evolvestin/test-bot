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

f = """emoji==1.7.0
aiogram==2.20
Pillow==9.1.0
heroku3==4.2.3
gspread==3.6.0
Unidecode==1.2.0
requests>=2.25.1
telegraph==1.4.0
selenium==3.141.0
GitPython==3.1.17
beautifulsoup4==4.9.3
pyTelegramBotAPI==4.5.1
google-api-python-client==1.10.0"""


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


while True:
    go = f.split('\n')
    os.system("echo Hello from the other side!")
    for i in go:
        install(i)
    print(f'Ушло на установку {len(go)} модулей', datetime.now().timestamp() - stamp, 'секунд')
    sleep(1000)
