import gspread
from time import sleep

while True:
    file = open('xstorage1.json').read()
    print(file)
    #acc = gspread.service_account('worker1.json')
    #files = acc.list_spreadsheet_files()
    #for i in files:
    #    print(i)
    sleep(100)
