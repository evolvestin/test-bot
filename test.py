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
packages = []

with open('go.txt') as file:
    requirements = file.read().split('\n')
    libraries = {re.sub('[~>=]=.*', '', line): re.sub('.*[~>=]=', '', line) for line in requirements}

with open('requirements.txt') as file:
    wrapper_requirements = file.read().split('\n')
    wrapper = {re.sub('[~>=]=.*', '', line): re.sub('.*[~>=]=', '', line) for line in wrapper_requirements}


for line in requirements:
    packages.append(line)

print(packages)

print('Все файлы выкачаны', packages, datetime.now().timestamp() - stamp)
sleep(10)


stamp = datetime.now().timestamp()
del wrapper, libraries, requirements, wrapper_requirements

while True:
    os.system('echo Hello from the other side!')
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    print(f'Ушло на установку {len(packages)} модулей', datetime.now().timestamp() - stamp, 'секунд')
    sleep(1000)
