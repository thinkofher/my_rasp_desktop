# run.py
# a file for testing classes
# future main file

from tools import MainMenu, MenuOption, lcd

prev_button = 26
ok_button = 19
cancel_button = 13
next_button = 6

if __name__ == '__main__':
    options = [
        MenuOption('tes1'),
        MenuOption('tes2')
    ]


    testmenu = MainMenu(
        lcd,
        prev_button = prev_button,
        next_button = next_button,
        ok_button = ok_button,
        cancel_button = cancel_button
    )

    for option in options:
        testmenu.add_menu_option(option)
        
    testmenu.main_loop()
