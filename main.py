import time
import homesecurity, lcd, button, status_led, arm_toggle, buzzer, motion, lock

led = status_led.StatusLED(13, 19, 26)
back_door = lock.DoorLock(17)

lcd.lcd_init()
button.setup()
motion.setup()
arm_toggle.setup()
homesecurity.outputs.add(lcd)
homesecurity.outputs.add(led)
homesecurity.outputs.add(back_door)
homesecurity.outputs.add(buzzer.Buzzer(4))

while True:
    lcd.update_status()
    led.update()
    time.sleep(1)