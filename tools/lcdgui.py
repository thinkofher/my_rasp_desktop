# tools/lcdgui.py

import RPi.GPIO as GPIO
from tools import (
    load_json_weather, save_json_file,
    load_json_file
    )
from pathlib import Path
from urllib.error import URLError


class MainMenu():

    def __init__(
        self, lcd_class,
        prev_button=0, next_button=0,
        cancel_button=0, ok_button=0
    ):
        
        self.__menu_options = []
        self.__lcd = lcd_class
        self.__actual_position = 0
        self.__should_close = False

        # settings of GPIO pins
        self.__pins = (
            prev_button,
            ok_button,
            cancel_button,
            next_button
        )
        GPIO.setmode(GPIO.BCM)
        for pin in self.__pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def main_loop(self):
        try:
            while True:
                if self.__should_close:
                    lcd.clear()
                    self.__lcd.message('Goodbye!')
                    time.sleep(2)
                    self.__lcd.clear()
                    break

                print(self.__actual_position)
                time.sleep(0.1)
                self.__lcd.clear()
                self.__show_options()

                # moving in menu
                if not GPIO.input(self.__pins[0]):
                    self.__previous_opt()
                    time.sleep(0.2)
                if not GPIO.input(self.__pins[3]):
                    self.__next_opt()
                    time.sleep(0.2)

                # choosing item
                if not GPIO.input(self.__pins[1]):
                    choosen_one = self.__menu_options[
                        self.__actual_position
                    ].get_name()
                    self.__lcd.clear()
                    self.__lcd.message(
                        'You choosed\n' +
                        choosen_one
                    )
                    time.sleep(2)

                # closing app
                if not GPIO.input(self.__pins[2]):
                    time.sleep(0.2)
                    self.__closing()

        except AttributeError:
            self.__lcd.clear()
            self.__lcd.message('NO OPTIONS')
    
    def add_menu_option(self, option):
        self.__menu_options.append(option)

    def __next_opt(self):
        self.__actual_position += 1
        if self.__actual_position > len(self.__menu_options)-1:
            self.__actual_position = len(self.__menu_options)-1
    
    def __previous_opt(self):
        self.__actual_position -= 1
        if self.__actual_position < 0:
            self.__actual_position = 0
            
    def __what_position(self):
        return self.__actual_position
        
    def __show_options(self):
        try:
            for i in range(len(self.__menu_options)):

                items_per_page = 4
                actual_page = int((self.__actual_position)/4)
                
                # Pagination
                if not(
                    i >= 0+(items_per_page*actual_page) and 
                        i < items_per_page+(items_per_page*actual_page)
                ):
                    continue

                actual_option = self.__menu_options[i]

                if i == self.__actual_position:
                    actual_option.set_signed()
                    message = actual_option.show()
                    self.__lcd.message(message)
                else:
                    actual_option.set_unsigned()
                    message = actual_option.show()
                    self.__lcd.message(message)

                # Keeping 2 items per line
                if (i+1)%2 == 0:
                    self.__lcd.message('\n')
                else:
                    self.__lcd.message('  ')

        except AttributeError:
            self.__lcd.clear()
            self.__lcd.message('NO OPTIONS')

    def __closing(self):
        while True:
            time.sleep(0.1)
            self.__lcd.clear()
            self.__lcd.message('Are you sure?')
            self.__lcd.message('\nB: Yes     R: No')
            
            # Choosed Yes
            if not GPIO.input(self.__pins[1]):
                self.__should_close = True
                time.sleep(0.2)
                break

            # Choosed No
            if not GPIO.input(self.__pins[2]):
                time.sleep(0.2)
                break


class MenuOption():

    def __init__(self, option_name):

        self.__option_name = option_name
        self.__if_signed = False
        # TODO: maybe higher order func?
        # self.__action = action

    def get_name(self):
        return self.__option_name

    def set_signed(self):

        self.__if_signed = True

    def set_unsigned(self):

        self.__if_signed = False

    def change_status(self):

        self.__if_signed = not self.__if_signed

    def show(self):

        if self.__if_signed:
            return '[*]{}'.format(
                self.__option_name
                )
        else:
            return '[_]{}'.format(
                self.__option_name
                )


class CityOption(MenuOption):

    def __init__(self, city, secret_key, visible_name=False):

        self.__option_name = city['name']

        if visible_name:
            self.__option_name = visible_name

        if len(self.__option_name) > 4:
            self.__option_name = self.__option_name[0:4]

        self.__if_signed = False
        self.__latitude = city['latitude']
        self.__longitude = city['longitude']

        self.__weather_api_url = "https://api.darksky.net/forecast/{}/{},{}?{}".format(
            secret_key,
            self.__latitude,
            self.__longitude,
            'units=si'
            )
        self.__old_data_path = Path(
            'data/{}.json'.format(
                self.__option_name
            )
        )
        self.__noData = True

    def weather_json(self):
        try:
            self.__json_weather = load_json_weather(
                self.__weather_api_url
                )
            save_json_file(
                self.__json_weather, self.__old_data_path
                )
            self.__isOffline = False
            self.__noData = False
        except URLError:
            try:
                self.__json_weather = load_json_file(
                    self.__old_data_path
                )
                self.__isOffline = True
                self.__noData = False
            except FileNotFoundError:
                self.__noData = True
                
    
    def is_Offline(self):
        return self.__isOffline
        
    def is_Data(self):
        return not self.__noData
