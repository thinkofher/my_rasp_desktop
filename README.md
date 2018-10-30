# My Raspberry Pi Desktop App

![](https://github.com/thinkofher/my_rasp_desktop/blob/master/data/visual.JPG)

## Description
Small application, developed for learning purposes and fun. The main reason for creating this thing was to have something to show actual weather and time. It is also looking cool on a desk. You can easly add your own city to [```cities.json```](https://github.com/thinkofher/my_rasp_desktop/blob/master/data/cities.json), create [Dark Sky API](https://darksky.net/dev) account and run the app.

## Configure
To use this app you have to create ```secret_key.json``` file in [data](https://github.com/thinkofher/my_rasp_desktop/tree/master/data) folder. It should look like following:
```javascript
{
    "secret":"your_secret_darksky_api_key"
}
```

## Features
- downloading json weather data from [Dark Sky API](https://darksky.net/dev)
- display the time with an accuracy of one second (super cool)
- can choose from different cities with a help of buttons
- deployed with tools for creating lcd gui

## Requirements
- [Python 3.6.x](https://gist.github.com/dschep/24aa61672a2092246eaca2824400d37f)
- [Adafruit_Python_CharLCD](https://github.com/adafruit/Adafruit_Python_CharLCD)
- [Dark Sky API](https://darksky.net/dev) account
- Raspberry Pi (tested on 3 b+, give me to know if you deployed it on older versions)
- 16x2 LCD display
- Wires and stuff

## TODO list
- show how many unseen mails you have at your mailbox
- fix bad refreshing