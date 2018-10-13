# weather.py

import json
from datetime import datetime
from tools import (
    load_json_file, save_json_file, current_time, load_json_weather
    )
from pathlib import Path


secretkeyPath = Path('data/secret_key.json')
lastdataPath = Path('data/last_data.json')
cities = Path('data/cities.json')

citiDict = load_json_file(cities)
city = citiDict['Lodz']

try:
    with open(secretkeyPath, 'r') as key:
        secret_key = json.loads(key.read())['secret']
except FileNotFoundError:
    secret_key = input("Please enter you secret key: ")
    new_json_file = {
        "secret": secret_key
    }
    with open(secretkeyPath, 'w') as file:
        file.write(json.dumps(new_json_file, indent=2))

weather_api_url = "https://api.darksky.net/forecast/{}/{},{}?{}".format(
    secret_key,
    city['latitude'],
    city['longitude'],
    'units=si'
)

data = load_json_weather(weather_api_url)

current_data = data['currently']
time_of_downloads = data['currently']['time']
time_of_downloads = datetime.fromtimestamp(
    int(time_of_downloads)
    ).strftime("%A, %B %d, %Y %H:%M:%S")

print(
    "Actual teperature in {} is {} Celcius degrees.".format(
        city['name'],
        round(float(current_data['temperature']))
    )
)

print('Actualization from {}'.format(
        time_of_downloads
    )
)

save_json_file(lastdataPath, data)

while (True):
    last_data = load_json_file(lastdataPath)
    time_of_download = int(
        last_data['currently']['time']
    )
    if current_time() >= time_of_download+60:
        data = load_json_weather(weather_api_url)
        save_json_file(lastdataPath, data)

        print(
           "Actual teperature in {} is {} Celcius degrees.".format(
                city['name'],
                round(float(data['currently']['temperature']))
            )
        )

        print('Actualization from {}'.format(
                datetime.fromtimestamp(
                    int(data['currently']['time'])
                    ).strftime("%A, %B %d, %Y %H:%M:%S")
            )
        )
