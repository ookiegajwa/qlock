import homesecurity
import rpi_gpio as GPIO

# Duty cycle percentage for servo at 0-degree position
MIN_DUTY_CYCLE = 2.5
# Duty cycle percentage for servo at 180-degree position
MAX_DUTY_CYCLE = 12.5


class DoorLock():

    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin

        GPIO.setup(gpio_pin, GPIO.OUT)
        pwm = GPIO.PWM(gpio_pin, 50, mode = GPIO.PWM.MODE_MS)
        pwm.ChangeDutyCycle(2.5)

    def on_arm(self):
        self.pwm.ChangeDutyCycle(12.5)
    def on_disarm(self):
        self.pwm.ChangeDutyCycle(2.5)

    def update(self):
        pass