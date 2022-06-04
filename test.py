import re
import os
import requests
import _thread
import gspread
import subprocess
import sys
from time import sleep
from typing import Union
import concurrent.futures
from datetime import datetime
os.environ['DEBUSSY'] = 'l'
stamp = datetime.now().timestamp()


def environmental_files():
    created_files, local_files = [], os.listdir('.')
    for key in os.environ.keys():
        key = key.lower()
        if key.endswith('.json'):
            created_files.append(key)
            if key not in local_files:
                with open(key, 'w') as file:
                    file.write(os.environ.get(key))
    return created_files


def package_install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


def get_environ(update_gspread: Union[bool, str]):
    print('загружаем таблицы')
    table = gspread.service_account('environ.json').open('heroku cloud').worksheet('environ').get('A1:Z50000')
    if update_gspread:
        print('Обновляем gspread')
        _thread.start_new_thread(package_install, (update_gspread,))
    print('Таблицы загружены', table[0])


def package_handler():
    packages, update_gspread = [], False
    with open('go.txt') as file:
        requirements = file.read().split('\n')

    with open('requirements.txt') as file:
        wrapper_requirements = file.read().split('\n')
        wrapper = {re.sub('[~>=]=.*', '', line): re.sub('.*[~>=]=', '', line) for line in wrapper_requirements}

    for line in requirements:
        install = True if line and line not in wrapper_requirements else None
        search, library_name = re.search('([!~>=])=(.*)', line), re.sub('[~>=]=.*', '', line)
        if line and line not in wrapper_requirements and search:
            if library_name in wrapper and search.group(1) in ['=', '>']:
                version = int(re.sub(r'\D', '', search.group(2)))
                wrapper_version = int(re.sub(r'\D', '', wrapper[library_name]) or '0')
                install = False if wrapper_version >= version else install
        packages.append(line) if install and library_name != 'gspread' else None
        update_gspread = line if library_name == 'gspread' and install is True else update_gspread
    return packages, update_gspread


def start_wrapper():
    while True:
        environmental_files()
        libraries, update_gspread = package_handler()
        print('Все файлы выкачаны', libraries, datetime.now().timestamp() - stamp)
        os.system('echo Hello from the other side!')
        _thread.start_new_thread(get_environ, (update_gspread,))
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as future_executor:
            [future_executor.submit(package_install, library) for library in libraries]
        print(f'Ушло на установку {len(libraries)} модулей', datetime.now().timestamp() - stamp, 'секунд')
        sleep(1000)


if __name__ == '__main__':
    start_wrapper()
