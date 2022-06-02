import gspread
import re
import os
from bs4 import BeautifulSoup
import requests
import _thread
import telebot
import subprocess
import sys
from time import sleep
from telegraph import upload
from time import sleep
from datetime import datetime
os.environ["DEBUSSY"] = 'l'
stamp = datetime.now().timestamp()
downloads = []

with open('go.txt') as file:
    requirements = file.read()


def install(pack):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pack])


for package in requirements.split('\n'):
    search = re.search('[!~>=]=(.*)', package)
    version = search.group(1) if search else None
    library_name = re.sub('[~>=]=.*', '', package)
    query = BeautifulSoup(requests.get(f'https://pypi.org/simple/{library_name}/').text, 'html.parser')
    links = query.find_all('a', text=f"{library_name}-{version}.tar.gz") if version else query.find_all('a')
    download_link = links[-1].get('href') if links else None
    if download_link:
        print(download_link)
        download = requests.get(download_link, stream=True)
        with open(f'{library_name}-{version}.tar.gz', 'wb') as f:
            for chunk in download:
                f.write(chunk)
        downloads.append(f'{library_name}-{version}.tar.gz')

print('Все файлы выкачаны', downloads, datetime.now().timestamp() - stamp)
sleep(50)

stamp = datetime.now().timestamp()


while True:
    os.system("echo Hello from the other side!")
    for i in downloads:
        install(i)
    print(f'Ушло на установку {len(downloads)} модулей', datetime.now().timestamp() - stamp, 'секунд')
    sleep(1000)
