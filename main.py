import time
import homesecurity, lcd, status_led

lcd.lcd_init()

while True:
    lcd.update_status()
    time.sleep(1)