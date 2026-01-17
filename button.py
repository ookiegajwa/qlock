import homesecurity as hs
import rpi_gpio as GPIO

BUTTON_PIN = 23
my_sensor = hs.Sensor(zone=1)

def setup():
    hs.sensors.add(my_sensor)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=buttonPressed)

def buttonPressed(channel):
    if GPIO.input(channel) == GPIO.LOW:
        hs.trip(my_sensor)
    else:
        hs.clear(my_sensor)
