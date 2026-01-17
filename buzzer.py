import homesecurity
import rpi_gpio as GPIO
import time

class Buzzer(homesecurity.SimpleOutput):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

    def on_arm(self):
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(self.pin, GPIO.LOW)

    def on_disarm(self):
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.15)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.15)
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.15)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.15)

    def on_alarm(self):
        GPIO.output(self.pin, GPIO.HIGH)