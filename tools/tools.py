# tools/tools.py

import json
from urllib.request import urlopen
from string import ascii_uppercase, digits
from random import choice
from datetime import datetime
from math import floor


def random_key(length):
    '''
    Creating random string with given length.
    '''
    key = ''.join(
        choice((ascii_uppercase + digits)) for _ in range(length)
    )
    return key


def load_json_file(path):
    '''
    Returning dictionary from given path
    of json file.
    '''
    with open(path) as file:
        jsonfile = json.loads(file.read())
    return jsonfile


def save_json_file(path, jsonVar):
    '''
    Save dict in json file in given path.
    '''
    with open(path, 'w') as file:
        file.write(json.dumps(jsonVar, indent=2))
    return 0


def load_json_weather(url):
    '''
    Returning json with weather information
    from dark sky API.
    '''
    with urlopen(url) as response:
        source = json.loads(response.read())
    return source


def current_time():
    '''
    Returning current time.
    '''
    return floor(
        datetime.now().timestamp()
    )
