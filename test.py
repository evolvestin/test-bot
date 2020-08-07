import os
import sys
from time import sleep

os.system('python setup.py sdist')
os.system('twine upload --repository-url https://upload.pypi.org/legacy/ dist/* '
          '--username evolvestin --password NAEzZ_4sF$9c*#@MUX$H7X8^k=vkRB')
sleep(3600)
