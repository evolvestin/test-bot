import re
import os
import sys
import stat
import shutil
import gspread
import heroku3
import warnings
import subprocess
from time import sleep
import concurrent.futures
from git.repo.base import Repo
from datetime import datetime, timezone, timedelta
stamp = datetime.now().timestamp()


def package_installer(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


def delete(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)
    return action, name, exc


def log_handler(logs, key: str):
    tz, response = timezone(timedelta(hours=3)), False
    for log in reversed(logs.split('\n')):
        if key in log:
            search = re.search(r'(.*\+00:00)', log)
            date = datetime.fromisoformat(search.group(1)) if search else None
            if date >= datetime.now(tz) - timedelta(minutes=5):
                response = True
                break
    return response


def environ_installer():
    warnings.simplefilter('ignore')
    app, environ, packages = None, False, []
    for app in heroku3.from_key(os.environ['api']).apps():
        pass
    for key, value in os.environ.items():
        if key.lower().endswith('.json') and key.lower() not in os.listdir('.'):
            with open(key.lower(), 'w') as file:
                file.write(value)
    with open('requirements.txt') as file:
        wrapper_requirements = file.read().split('\n')
        wrapper = {re.sub('[~>=]=.*', '', line): re.sub('.*[~>=]=', '', line) for line in wrapper_requirements}

    idle = log_handler(app.get_log(lines=1000), 'initialize with idling')
    table = gspread.service_account('environ.json').open('heroku cloud').worksheet('environ').get('A1:Z50000')
    keys, api_row_id, api_columns, script_key_id, var_columns, repo_columns = table.pop(0), None, [], None, [], {}
    for key_id in range(len(keys)):
        api_columns.append(key_id) if keys[key_id].startswith('api') else None
        var_columns.append(key_id) if keys[key_id].startswith('var') else None
        script_key_id = key_id if keys[key_id].startswith('script') else script_key_id
        repo_columns.update({'link': key_id}) if keys[key_id] == 'repository' else None
        repo_columns.update({'key': key_id}) if keys[key_id] == 'repository-key' else None
    for row_id in range(len(table)):
        for key_id in api_columns:
            if key_id < len(table[row_id]) and os.environ['api'] == table[row_id][key_id]:
                api_row_id = row_id

    if api_row_id is not None:
        repo, variables, script_name = {}, {}, None
        if script_key_id is not None and script_key_id < len(table[api_row_id]):
            script_name = table[api_row_id][script_key_id]

        for key in ['key', 'link']:
            if repo_columns.get(key) is not None and repo_columns[key] < len(table[api_row_id]):
                repo[key] = table[api_row_id][repo_columns[key]]

        for col_id in var_columns:
            if col_id < len(table[api_row_id]):
                variables.update({col_id: table[api_row_id][col_id]})

        for col_id, value in variables.items():
            regex = re.sub('var=', '', keys[col_id], 1) if 'var=' in keys[col_id] else None
            for item in re.findall(regex, value) if regex else []:
                if type(item) == tuple and len(item) == 2:
                    os.environ[item[0].strip()] = item[1].strip()

        link = repo.get('link')
        if repo.get('key') and repo.get('link'):
            link = f"https://{repo['key']}:x-oauth-basic@{re.sub('http.*?://', '', repo['link'])}"
        if link:
            Repo.clone_from(link, 'temp')
            os.makedirs('temp/.git', exist_ok=True), shutil.rmtree('temp/.git', onerror=delete)
            for file_name in os.listdir('temp'):
                paths = f'temp/{file_name}', file_name
                shutil.copytree(*paths) if os.path.isdir(paths[0]) else shutil.copy(*paths)
            shutil.rmtree('temp', onerror=delete)
            environ = True
        if script_name and script_name in os.listdir():
            os.rename(script_name, 'main.py')

    with open('requirements.txt') as file:
        for line in file.read().split('\n'):
            install = True if line and line not in wrapper_requirements else None
            search, library_name = re.search('([!~>=])=(.*)', line), re.sub('[~>=]=.*', '', line)
            if line and line not in wrapper_requirements and search:
                if library_name in wrapper and search.group(1) in ['=', '>']:
                    version = int(re.sub(r'\D', '', search.group(2)))
                    wrapper_version = int(re.sub(r'\D', '', wrapper[library_name]) or '0')
                    install = False if wrapper_version >= version else install
            packages.append(line) if install else None

    if environ is False:
        print('Initialize fail. Cannot find repository link.')
    elif 'main.py' not in os.listdir():
        environ = False
        print('Initialize fail. Cannot find main.py.')
    while environ is False:
        pass

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as future_executor:
        [future_executor.submit(package_installer, package) for package in packages]
    print(f'Successful initialized. Handled {len(packages)} packages for {datetime.now().timestamp() - stamp} sec.')

    if idle:
        print('Idling. ')
        idle_stamp = datetime.now().timestamp()
        while log_handler(app.get_log(lines=1000), 'stop idling') is False:
            sleep(1)
        print(f'Idling stopped after {datetime.now().timestamp() - idle_stamp} sec. Launching.')
    else:
        print('Configured without idling. Launching.')


if __name__ == '__main__':
    environ_installer()
    from main import start
    start(stamp)
