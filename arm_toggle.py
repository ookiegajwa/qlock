import homesecurity as hs
import rpi_gpio as GPIO

BUTTON_PIN = 24

def setup():
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=buttonPressed)

def buttonPressed(channel):
    print("toggle arm")
    hs.toggle_arm()

