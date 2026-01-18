import homesecurity
import rpi_gpio as GPIO

class DoorLock(homesecurity.SimpleOutput):

    def __init__(self, gpio_pin):
        GPIO.setmode(GPIO.BCM)
        self.gpio_pin = gpio_pin

        GPIO.setup(gpio_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(gpio_pin, 50, mode = GPIO.PWM.MODE_MS)
        self.pwm.ChangeDutyCycle(2.5)

    def on_arm(self):
        self.pwm.ChangeDutyCycle(12.5)
    def on_disarm(self):
        self.pwm.ChangeDutyCycle(2.5)
    def on_alarm(self):
        pass

    def update(self):
        pass