import rpi_gpio as GPIO

GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.output(26, GPIO.LOW)
GPIO.output(19, GPIO.LOW)
GPIO.output(13, GPIO.LOW)

def on_arm():
    GPIO.output(26, GPIO.LOW)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
def on_disarm():
    GPIO.output(26, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(13, GPIO.HIGH)
def on_alarm():
    GPIO.output(26, GPIO.HIGH)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)