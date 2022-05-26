from datetime import time

class CheckInSystemConfig:

    # min
    BEFORE_CLOCK = 15
    AFTER_CLOCK = 30
    WINDOW_INTERVAL = 1
    WORKING_TIME_INTERVAL = 30

    # hour
    # WARNING: Cannot set to min, unless modify main.py first
    NON_WORKING_TIME_INTERVAL = 1

    def __init__(self, clockin = time(9), clockout = time(18)):
        self.clockinTime = clockin
        self.clockoutTime = clockout