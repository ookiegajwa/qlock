import homesecurity as hs
import rpi_gpio as GPIO

MOTION_PIN = 16
my_sensor = hs.Sensor(2, False)

def setup():
    hs.sensors.add(my_sensor)
    GPIO.setup(MOTION_PIN, GPIO.IN)
    GPIO.add_event_detect(MOTION_PIN, GPIO.BOTH, callback=buttonPressed)

def buttonPressed(channel):
    if GPIO.input(channel) == GPIO.HIGH:
        hs.trip(my_sensor)
    else:
        hs.clear(my_sensor)
