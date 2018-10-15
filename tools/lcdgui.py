# tools/lcdgui.py

import RPi.GPIO as GPIO
from tools import (
    load_json_weather, save_json_file,
    load_json_file, current_time
    )
from pathlib import Path
from urllib.error import URLError
from datetime import datetime
import abc
import time


class Menu(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError(
            'You have to define __init__ method!'
        )

    @abc.abstractmethod
    def main_loop(self):
        raise NotImplementedError(
            'You have to define __show_options method!'
        )

    @abc.abstractmethod
    def _show_options(self):
        raise NotImplementedError(
            'You have to define __show_options method!'
        )

    @abc.abstractmethod
    def _closing(self):
        raise NotImplementedError(
            'You have to define __closing method!'
        )

    def add_menu_option(self, option):
        self._menu_options.append(option)

    def _next_opt(self):
        self._actual_position += 1
        if self._actual_position > len(self._menu_options)-1:
            self._actual_position = len(self._menu_options)-1

    def _previous_opt(self):
        self._actual_position -= 1
        if self._actual_position < 0:
            self._actual_position = 0

    def what_position(self):
        return self._actual_position

    def _show_options(self):
        try:
            for i in range(len(self._menu_options)):

                items_per_page = 4
                actual_page = int((self._actual_position)/4)

                # Pagination
                if not(
                    i >= 0+(items_per_page*actual_page) and
                        i < items_per_page+(items_per_page*actual_page)
                ):
                    continue

                actual_option = self._menu_options[i]

                if i == self._actual_position:
                    actual_option.set_signed()
                    message = actual_option.show()
                    self._lcd.message(message)
                else:
                    actual_option.set_unsigned()
                    message = actual_option.show()
                    self._lcd.message(message)

                # Keeping 2 items per line
                if (i+1)%2 == 0:
                    self._lcd.message('\n')
                else:
                    self._lcd.message('  ')

        except AttributeError:
            self._lcd.clear()
            self._lcd.message('NO OPTIONS')


class MainMenu(Menu):


    def __init__(
        self, lcd_class, prev_button=0,
        next_button=0, cancel_button=0,
        ok_button=0, subMenu = False
    ):
        self.__wait_time = 5*60
        self._menu_options = []
        self._lcd = lcd_class
        self._actual_position = 0
        self._should_close = False

        if subMenu:
            self.__subMenu = subMenu
        else:
            self.__subMenu = False

        # settings of GPIO pins
        self._pins = (
            prev_button,
            ok_button,
            cancel_button,
            next_button
        )
        GPIO.setmode(GPIO.BCM)
        for pin in self._pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def main_loop(self):
        try:
            while True:
                if self._should_close:
                    self._lcd.clear()
                    self._lcd.message('Goodbye!')
                    time.sleep(2)
                    self._lcd.clear()
                    break

                # print(self._actual_position) for testing purposes
                time.sleep(0.2)
                self._show_status()

                # TODO: maybe just delete this?
                if not GPIO.input(self._pins[0]):
                    time.sleep(0.2)
                    pass
                if not GPIO.input(self._pins[3]):
                    time.sleep(0.2)
                    pass

                # choosing item
                if not GPIO.input(self._pins[1]):
                    time.sleep(0.2)
                    try:
                        self.__subMenu.main_loop()
                    except NameError:
                        pass

                # closing app
                if not GPIO.input(self._pins[2]):
                    time.sleep(0.2)
                    self._closing()

        except AttributeError:
            self._lcd.clear()
            self._lcd.message('NO OPTIONS 1')

    def _closing(self):
        while True:
            time.sleep(0.2)
            self._lcd.clear()
            self._lcd.message('Are you sure?')
            self._lcd.message('\nB: Yes     R: No')

            # Choosed Yes
            if not GPIO.input(self._pins[1]):
                self._should_close = True
                time.sleep(0.2)
                break

            # Choosed No
            if not GPIO.input(self._pins[2]):
                time.sleep(0.2)
                break

    def _updatae_time(self):
        self.__curr_time = datetime.fromtimestamp(
                current_time()
            ).strftime("%H:%M:%S")

    def _show_status(self):
        self._updatae_time()
        
        # updating data
        try:
            if current_time() >= (
                self.__subMenu.get_actual_city_down_time() +
                    (self.__wait_time)
            ):
                self.__subMenu.update_city_data()
        
        # offline and no old data
        except TypeError:
            pass

        try:
            self._status_message = '{} {}{}C\n{}'.format(
                self.__subMenu.get_actual_city_full_name(),
                self.__subMenu.get_actual_city_temp(),
                chr(223),
                self.__curr_time
            )

        # No old data
        except (AttributeError, TypeError):
            self._status_message = '{} NO DATA\n{}'.format(
                self.__subMenu.get_actual_city_full_name(),
                self.__curr_time
            )
        self._lcd.clear()
        self._lcd.message(
            self._status_message
        )

        if self.__subMenu.is_Offline_actual_city():
            self._lcd.message(' OFFLINE')
            
            # maybe is offline now?
            self.__subMenu.update_city_data()


class WeatherMenu(MainMenu):


    # added new __init__ because of self.__first_city
    # TODO: find some magic to fix this
    def __init__(
        self, lcd_class, prev_button=0,
        next_button=0, cancel_button=0,
        ok_button=0, subMenu = False
    ):
        self._menu_options = []
        self._lcd = lcd_class
        self._actual_position = 0
        self._should_close = False
        self.__first_city = True

        if subMenu:
            self.__subMenu = subMenu
        else:
            self.__subMenu = False

        # settings of GPIO pins
        self._pins = (
            prev_button,
            ok_button,
            cancel_button,
            next_button
        )
        GPIO.setmode(GPIO.BCM)
        for pin in self._pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    # like above, beacause of self.__first_city
    def add_menu_option(self, option):
        self._menu_options.append(option)
        if self.__first_city:
            self._actual_city = self._menu_options[
                self._actual_position
            ]
            self.__first_city = False
            self.update_city_data()


    def main_loop(self):
        self._actual_position = 0
        try:
            while not self._should_close:

                time.sleep(0.1)
                self._lcd.clear()
                self._show_options()

                # moving in menu
                if not GPIO.input(self._pins[0]):
                    self._previous_opt()
                    time.sleep(0.2)
                if not GPIO.input(self._pins[3]):
                    self._next_opt()
                    time.sleep(0.2)

                # choosing item
                if not GPIO.input(self._pins[1]):
                    time.sleep(0.2)
                    self._actual_city = self._menu_options[
                        self._actual_position
                    ]
                    self._lcd.clear()
                    self._lcd.message(
                        'You choosed\n' +
                        self.get_actual_city_full_name()
                    )
                    self.update_city_data()
                    time.sleep(2)
                    break

                # closing app
                if not GPIO.input(self._pins[2]):
                    time.sleep(0.2)
                    self._closing()

        except AttributeError:
            self._lcd.clear()
            self._lcd.message('NO OPTIONS 2')

        # to run again after closing!
        self._should_close = False

    def _closing(self):
        self._should_close = True

    def get_actual_city_name(self):

        return self._actual_city.get_name()

    def get_actual_city_temp(self):

        return self._actual_city.current_temp()

    def get_actual_city_full_name(self):

        return self._actual_city.get_city_full_name()
    
    def get_actual_city_down_time(self):
        
        return self._actual_city.get_city_download_time()
        
    def update_city_data(self):
        self._actual_city.weather_json()
    
    def is_Offline_actual_city(self):
        return self._actual_city.is_Offline()
    
    def is_Data_actual_city(self):
        return self._actual_city.check_data()


class MenuOption(object):


    def __init__(self, option_name):

        self._option_name = option_name
        self._if_signed = False
        # TODO: maybe higher order func?
        # self.__action = action

    def get_name(self):
        return self._option_name

    def set_signed(self):

        self._if_signed = True

    def set_unsigned(self):

        self._if_signed = False

    def change_status(self):

        self._if_signed = not self._if_signed

    def show(self):

        if self._if_signed:
            return '[*]{}'.format(
                self._option_name
                )
        else:
            return '[_]{}'.format(
                self._option_name
                )


class CityOption(MenuOption):


    def __init__(self, city, secret_key, visible_name=False, full_name=False):

        self._option_name = city['name']

        if full_name:
            self._city_full_name = city['name']

        if visible_name:
            self._option_name = visible_name

        if len(self._option_name) > 4:
            self._option_name = self._option_name[0:4]
        elif len(self._option_name) < 4:
            self._option_name = self._option_name + (
                4-len(self._option_name)
                )*' '

        self._if_signed = False
        self.__latitude = city['latitude']
        self.__longitude = city['longitude']

        self.__weather_api_url = "https://api.darksky.net/forecast/{}/{},{}?{}".format(
            secret_key,
            self.__latitude,
            self.__longitude,
            'units=si'
            )
        self._old_data_path = Path(
            'data/{}.json'.format(
                self._option_name
            )
        )
        self._json_weather = False
        self._isOffline = False

    def weather_json(self):
        try:
            self._json_weather = load_json_weather(
                self.__weather_api_url
                )
            save_json_file(
                self._old_data_path, self._json_weather
                )
            self._isOffline = False
            self._noData = False
        except URLError:
            try:
                self._isOffline = True
                self._json_weather = load_json_file(
                    self._old_data_path
                )
            except FileNotFoundError:
                self._isData = False


    def current_temp(self):

        if self._json_weather:
            return round(
                float(
                    self._json_weather['currently']['temperature']
                    )
                )
        else:
            self.weather_json()
            return round(
                float(
                    self._json_weather['currently']['temperature']
                    )
                )

    def get_city_full_name(self):
        return self._city_full_name

    def get_city_download_time(self):
        return int(
            self._json_weather['currently']['time']
        )
    
    def check_data(self):
        return self._isData
    
    def is_Offline(self):
        return self._isOffline
