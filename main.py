import time
import homesecurity, lcd, button, status_led

lcd.lcd_init()
button.setup()

while True:
    lcd.update_status()
    time.sleep(1)