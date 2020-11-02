import gspread
import os
import _thread
from time import sleep
directory = os.listdir('.')
os.environ["DEBUSSY"] = 'l'

m = os.environ.keys()
for i in m:
    print(i, '-', os.environ.get(i))

_thread.exit()

while True:
    #acc = gspread.service_account('worker1.json')
    #files = acc.list_spreadsheet_files()
    #for i in files:
    #    print(i)
    sleep(100)

