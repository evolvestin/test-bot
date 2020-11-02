import gspread
from time import sleep

while True:
    acc = gspread.service_account('xstorage1.json')
    files = acc.list_spreadsheet_files()
    for i in files:
        print(i)
    sleep(100)
