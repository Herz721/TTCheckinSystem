from datetime import time

Database = 'mysql+pymysql://root:********@localhost/TrojanTech'

class CheckInSystemConfig:
    # min < 60
    BEFORE_CLOCK = 15
    AFTER_CLOCK = 30
    WINDOW_INTERVAL = 1
    WORKING_TIME_INTERVAL = 30

    # hour
    # WARNING: Cannot set to min, unless modify main.py first
    NON_WORKING_TIME_INTERVAL = 1

    def __init__(self, clockin = "9", clockout = "18"):
        self.clockinTime = time(int(clockin))
        self.clockoutTime = time(int(clockout))