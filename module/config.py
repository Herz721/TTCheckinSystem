class CheckInSystemConfig:

    # min < 60
    BEFORE_CLOCK = 15
    AFTER_CLOCK = 30
    WINDOW_INTERVAL = 1
    WORKING_TIME_INTERVAL = 30

    # hour
    # WARNING: Cannot set to min, unless modify main.py first
    NON_WORKING_TIME_INTERVAL = 1

    def __init__(self, clockin, clockout):
        self.clockinTime = clockin
        self.clockoutTime = clockout