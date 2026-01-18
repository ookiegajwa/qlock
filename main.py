import time
import homesecurity, lcd, button, status_led, arm_toggle, buzzer, motion, lock
import sentry_sdk

sentry_sdk.init(
    dsn="https://a156bfaf9f2c6cddb4694a339b574c66@o4510728194883584.ingest.de.sentry.io/4510728333557840",
    send_default_pii=True,
)
led = status_led.StatusLED(5, 6, 26)
back_door = lock.DoorLock(13)

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
