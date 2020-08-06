import heroku3
import os
import _thread
from version import version as new_version


def drop():
    if os.environ.get('version') != new_version:
        if os.environ.get('api'):
            connection = heroku3.from_key(os.environ.get('api'))
            for app in connection.apps():
                config = app.config()
                config['version'] = new_version


if __name__ == '__main__':
    _thread.start_new_thread(drop, ())
