import time
import homesecurity, lcd

lcd.lcd_init()

while True:
    lcd.update_status()
    time.sleep(1)