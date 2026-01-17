# Store system state
state = 0  # 0=disarmed, 1=armed, 2=alarm
sensors = []
alarm = []
access_controls = []
outputs = []


# Classes for input/output events
class Sensor:
    def __init__(self, zone: int):
        self.zone = zone
        self.tripped = False


class AccessControl:
    def __init__(self, zone: int):
        self.zone = zone


class SimpleOutput:
    def on_arm(self):
        pass

    def on_disarm(self):
        pass

    def on_alarm(self):
        pass

def trip(sensor: Sensor):
    """Callback called when a sensor trips"""
    global state
    if state == 1:
        state = 2
        for output in outputs:
            output.on_alarm()
    if state != 0:
        alarm.append(sensor)
    sensor.tripped = True

def clear(sensor: Sensor):
    """Callback called when a sensor clears"""
    sensor.tripped = False


def toggle_arm(source: AccessControl):
    """Callback for when an access control device is authorized"""
    global state
    if state == 0:
        state = 1
        for output in outputs:
            output.on_arm()
    else:
        state = 0
        for output in outputs:
            output.on_disarm()
        alarm.clear()