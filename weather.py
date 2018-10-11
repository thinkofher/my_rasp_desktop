import json
from urllib.request import urlopen
from datetime import datetime

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

with urlopen(weather_api_url) as response:
    source = response.read()

data = json.loads(source)

current_data = data['currently']
time_of_downloads = data['currently']['time']
time_of_downloads = datetime.fromtimestamp(
    int(time_of_downloads)
    ).strftime("%A, %B %d, %Y %I:%M:%S")

print(
    "Actual teperature in Cracow is {} Celcius degrees.".format(
        round(float(current_data['temperature']))
    )
)

print('Actualization from {}'.format(
        time_of_downloads
    )
)
