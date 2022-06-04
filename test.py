import re
import os
import requests
import _thread
import subprocess
import sys
from time import sleep
from datetime import datetime
os.environ['DEBUSSY'] = 'l'
stamp = datetime.now().timestamp()


def package_install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


def package_handler():
    packages = []
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
        packages.append(line) if install else None
    return packages


while True:
    stamp = datetime.now().timestamp()
    libraries = package_handler()
    print('Все файлы выкачаны', libraries, datetime.now().timestamp() - stamp)
    os.system('echo Hello from the other side!')
    for library in libraries:
        _thread.start_new_thread(package_install, (library,))
    print(f'Ушло на установку {len(libraries)} модулей', datetime.now().timestamp() - stamp, 'секунд')
    sleep(1000)
