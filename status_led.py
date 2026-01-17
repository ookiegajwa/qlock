import homesecurity
import rpi_gpio as GPIO

class StatusLED(homesecurity.SimpleOutput):
    def __init__(self, disarmed_pin, armed_pin, alarm_pin):
        self.blink_state = False
        self.disarmed_pin = disarmed_pin
        self.armed_pin = armed_pin
        self.alarm_pin = alarm_pin

        GPIO.setup(alarm_pin, GPIO.OUT)
        GPIO.setup(armed_pin, GPIO.OUT)
        GPIO.setup(disarmed_pin, GPIO.OUT)
        GPIO.output(alarm_pin, GPIO.LOW)
        GPIO.output(armed_pin, GPIO.LOW)
        GPIO.output(disarmed_pin, GPIO.HIGH)

    def on_arm(self):
        GPIO.output(self.alarm_pin, GPIO.LOW)
        GPIO.output(self.armed_pin, GPIO.HIGH)
        GPIO.output(self.disarmed_pin, GPIO.LOW)
    def on_disarm(self):
        GPIO.output(self.alarm_pin, GPIO.LOW)
        GPIO.output(self.armed_pin, GPIO.LOW)
        GPIO.output(self.disarmed_pin, GPIO.HIGH)
    def on_alarm(self):
        GPIO.output(self.alarm_pin, GPIO.HIGH)
        GPIO.output(self.armed_pin, GPIO.LOW)
        GPIO.output(self.disarmed_pin, GPIO.LOW)

    def update(self):
        if homesecurity.state == 0:
            for sensor in homesecurity.sensors:
                if sensor.tripped:
                    GPIO.output(self.disarmed_pin, self.blink_state)
                    self.blink_state = not self.blink_state
                    return
            GPIO.output(self.disarmed_pin, GPIO.HIGH)
            self.blink_state = False