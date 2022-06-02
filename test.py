import gspread
import os
import _thread
import telebot
import subprocess
import sys
from telegraph import upload
from time import sleep
os.environ["DEBUSSY"] = 'l'

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    sleep(1000)

while True:
    os.system("echo Hello from the other side!")
    install('e-objects')
