import heroku3
import os
import _thread
from time import sleep
from version import version as new_version

while True:
    sleep(1)
    print('old', os.environ.get('version'))
    print('new', new_version)
    if os.environ.get('version') != new_version:
        if os.environ.get('api'):
            connection = heroku3.from_key(os.environ.get('api'))
            for app in connection.apps():
                config = app.config()
                config['version'] = new_version
