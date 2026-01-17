# Store system state
state = 0  # 0=disarmed, 1=armed, 2=alarm
sensors = set()
alarm = set()
access_controls = set()
outputs = set()


# Classes for input/output events
class Sensor:
    def __init__(self, zone: int, chime: bool):
        self.zone = zone
        self.tripped = False
        self.chime = chime


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

    def on_trip(self, sensor):
        pass

    def on_clear(self, sensor):
        pass

def trip(sensor: Sensor):
    """Callback called when a sensor trips"""
    global state
    if state == 1:
        state = 2
        for output in outputs:
            output.on_alarm()
    if state != 0:
        alarm.add(sensor)
    sensor.tripped = True
    for output in outputs:
        output.on_trip(sensor)

def clear(sensor: Sensor):
    """Callback called when a sensor clears"""
    sensor.tripped = False
    for output in outputs:
        output.on_clear(sensor)


def toggle_arm():
    """Callback for when an access control device is authorized"""
    print("sus")
    global state
    if state == 0:
        print("arming")
        state = 1
        for output in outputs:
            output.on_arm()
    else:
        print("disarming")
        state = 0
        for output in outputs:
            output.on_disarm()
        alarm.clear()