# tools/lcd/lcd.py

import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration:
lcd_rs = 27
lcd_en = 22
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(
    lcd_rs, lcd_en, lcd_d4,
    lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows
)
