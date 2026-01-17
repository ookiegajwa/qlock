import time
import homesecurity, lcd, button, status_led, arm_toggle, buzzer

lcd.lcd_init()
button.setup()
arm_toggle.setup()
homesecurity.outputs.append(lcd)
homesecurity.outputs.append(status_led)
homesecurity.outputs.append(buzzer.Buzzer(4))

while True:
    lcd.update_status()
    status_led.update()
    time.sleep(1)