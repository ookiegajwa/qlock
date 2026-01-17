# Store system state
armed = False
sensors = []
access_controls = []
outputs = []


# Classes for input/output events
class Sensor:
    def __init__(self, zone: int):
        # Setup is overridden by inheritors to set up the callbacks
        self.setup = None
        self.zone = zone


class AccessControl:
    def __init__(self, zone: int):
        self.setup = None
        self.zone = zone


class SimpleOutput:
    def __init__(self):
        self.setup = None
        self.alarm = None
        self.stop_alarm = None


def trip(sensor: Sensor):
    """Callback called when a sensor trips"""
    pass


def toggle_arm(source: AccessControl):
    """Callback for when an access control device is authorized"""
    pass