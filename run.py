# run.py
# a file for testing classes
# future main file

from tools import (
    MainMenu, WeatherMenu, lcd,
    CityOption, MenuOption,
    load_json_file, load_secret_key
)
from pathlib import Path

prev_button = 26
ok_button = 19
cancel_button = 13
next_button = 6

secretkeyPath = Path('data/secret_key.json')
cityPath = Path('data/cities.json')

cityData = load_json_file(cityPath)
secret_key = load_secret_key(secretkeyPath)

if __name__ == '__main__':

    subWMenu = WeatherMenu(
        lcd,
        prev_button=prev_button,
        next_button=next_button,
        ok_button=ok_button,
        cancel_button=cancel_button
    )

    for city in cityData:
        subWMenu.add_menu_option(
            CityOption(
                city=cityData[city],
                secret_key=secret_key,
                visible_name=cityData[city]['visible_name'],
                full_name=cityData[city]['name']
            )
        )

    testmenu = MainMenu(
        lcd,
        prev_button=prev_button,
        next_button=next_button,
        ok_button=ok_button,
        cancel_button=cancel_button,
        subMenu=subWMenu
    )

    testmenu.main_loop()
