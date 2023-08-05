import requests
from blackfynn import Blackfynn
from .config import API_TOKEN, API_SECRET
import os
import sys
import platform
if platform != "darwin":
    from .ui import DetailsInput
import progressbar

def env_keys_valid():
    if API_TOKEN != 'local-api-key' and API_SECRET != 'local-secret-key':
        return True
    return False

def arg_valid():
    if len(sys.argv) == 1:
        return False
    if len(sys.argv[1].split('-')) == 5 and len(sys.argv[2].split('-')) == 5:
        return True
    return False

def run():

    if env_keys_valid():
        api_token = API_TOKEN
        api_secret = API_SECRET
        collection = sys.argv[1]
    elif arg_valid():
        api_token = sys.argv[1]
        api_secret = sys.argv[2]
        collection = sys.argv[3]
    elif len(sys.argv) == 1:
        if platform == "darwin":
            print('Sorry, tkinter in MacOS is not supported :(. Please use the CLI options')
            return
        ui = DetailsInput()
        api_token, api_secret, collection = ui.values()

    bf = Blackfynn(api_token=api_token,api_secret=api_secret)
    print('Connected to Blackfynn')
    print('Looking for Collection...')
    col = get_folder_items(bf, collection)
    print('Collection found. Staring file downloads...')
    try:
        os.mkdir(col.name)
    except FileExistsError:
        pass

    for item in progressbar.progressbar(col.items):
        if 'files' in dir(item):
            for file in item.files:
                file_type = get_file_type(file.s3_key)
                s3_url = file.url
                response = requests.get(s3_url)
                if response.status_code == 200:
                    sys.stdout.write('\rDownloading file: %s' % file.name)
                    f = open(col.name + '/' + file.name + file_type, 'wb')
                    f.write(response.content)
                    sys.stdout.flush()

def get_file_type(s3_url):
    if len(s3_url.split('.')) == 2:
        return ''
    return s3_url.split('.')[-1]

def get_folder_items(bf, name):
    if 'dataset' in name:
        return bf.get_dataset(name)
    return bf.get(name)