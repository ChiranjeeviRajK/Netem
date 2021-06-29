import lcddriver
from time import *
import time
import touch
display = lcddriver.lcd()
n = touch.TOUCH()

try:
   while True:
        print("Touch now")
        num = n.keypad()
        print("Writing to display-------"+num)
        num = ''
        print("Writing to display")
        #display.lcd_display_string("Settings", 1)
        display.lcd_display_string("Settings         >",1)

        display.lcd_display_string("Status", 2)
        time.sleep(2)
        display.lcd_display_string("Monitor", 1)
        display.lcd_display_string("Tests", 2)
        time.sleep(2)
        display.lcd_clear()
        time.sleep(2)

except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()
