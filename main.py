import time
import homesecurity, lcd, button, status_led, arm_toggle

homesecurity.outputs.append(lcd)
lcd.lcd_init()
button.setup()
arm_toggle.setup()
homesecurity.outputs.append(status_led)

while True:
    lcd.update_status()
    status_led.update()
    time.sleep(1)