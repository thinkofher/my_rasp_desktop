# weather.py

import json
from datetime import datetime
from tools import (
    load_json_file, save_json_file, current_time, load_json_weather
    )

Cracow = {
    "latitude": 50.0646,
    "longitude": 19.9449
}

try:
    with open("secret_key.json", 'r') as key:
        secret_key = json.loads(key.read())['secret']
except FileNotFoundError:
    secret_key = input("Please enter you secret key: ")
    new_json_file = {
        "secret": secret_key
    }
    with open("secret_key.json", 'w') as file:
        file.write(json.dumps(new_json_file, indent=2))

weather_api_url = "https://api.darksky.net/forecast/{}/{},{}?{}".format(
    secret_key,
    Cracow['latitude'],
    Cracow['longitude'],
    'units=si'
)

data = load_json_weather(weather_api_url)

current_data = data['currently']
time_of_downloads = data['currently']['time']
time_of_downloads = datetime.fromtimestamp(
    int(time_of_downloads)
    ).strftime("%A, %B %d, %Y %H:%M:%S")

print(
    "Actual teperature in Cracow is {} Celcius degrees.".format(
        round(float(current_data['temperature']))
    )
)

print('Actualization from {}'.format(
        time_of_downloads
    )
)

save_json_file('last_data.json', data)

while (True):
    last_data = load_json_file('last_data.json')
    time_of_download = int(
        last_data['currently']['time']
    )
    if current_time() >= time_of_download+60:
        data = load_json_weather(weather_api_url)
        save_json_file('last_data.json', data)

        print(
           "Actual teperature in Cracow is {} Celcius degrees.".format(
                round(float(data['currently']['temperature']))
            )
        )

        print('Actualization from {}'.format(
                datetime.fromtimestamp(
                    int(data['currently']['time'])
                    ).strftime("%A, %B %d, %Y %H:%M:%S")
            )
        )
