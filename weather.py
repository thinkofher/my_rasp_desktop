# weather.py

from datetime import datetime
from pathlib import Path
from tools import (
    load_json_file, save_json_file,
    load_json_weather, load_secret_key,
    current_time
    )


secretkeyPath = Path('data/secret_key.json')
lastdataPath = Path('data/last_data.json')
cities = Path('data/cities.json')

citiDict = load_json_file(cities)
city = citiDict['Lodz']

secret_key = load_secret_key(secretkeyPath)
weather_api_url = "https://api.darksky.net/forecast/{}/{},{}?{}".format(
    secret_key,
    city['latitude'],
    city['longitude'],
    'units=si'
)

data = load_json_weather(weather_api_url)

print(
    "Actual teperature in {} is {} Celcius degrees.".format(
        city['name'],
        round(float(data['currently']['temperature']))
    )
)

print('Actualization from {}.'.format(
        datetime.fromtimestamp(
            int(data['currently']['time'])
            ).strftime("%A, %B %d, %Y %H:%M:%S")
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

        print('Actualization from {}.'.format(
                datetime.fromtimestamp(
                    int(data['currently']['time'])
                    ).strftime("%A, %B %d, %Y %H:%M:%S")
            )
        )
