#lcdgui.py
import RPi.GPIO as GPIO
import time


class MainLoop():

    def __init__(self, lcd_class, pin_1, pin_2, pin_3):

        self.__lcd = lcd_class

        # setting
        self.__pins = (
            pin_1,
            pin_2,
            pin_3
        )
        GPIO.setmode(GPIO.BCM)
        for pin in self.__pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class MenuOption():

    def __init__(self, option_name):

        self.__option_name = option_name
        self.__if_signed = False

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
            return '[ ]{}'.format(
                self.__option_name
                )

class CityOption(MenuOption):

    def __init__(self, city, visible_name=False):

        self.__option_name = city['name']

        if visible_name:
            self.__option_name = visible_name

        if len(self.__option_name) > 4:
            self.__option_name = self.__option_name[0:4]

        self.__if_signed = False
        self.__latitude = city['latitude']
        self.__longitude = city['longitude']

    def weather_json(self):
        pass
