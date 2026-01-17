import time
import homesecurity, lcd, button, status_led, arm_toggle, buzzer, motion

led = status_led.StatusLED(13, 19, 26)

lcd.lcd_init()
button.setup()
motion.setup()
arm_toggle.setup()
homesecurity.outputs.append(lcd)
homesecurity.outputs.append(led)
homesecurity.outputs.append(buzzer.Buzzer(4))

while True:
    lcd.update_status()
    led.update()
    time.sleep(1)