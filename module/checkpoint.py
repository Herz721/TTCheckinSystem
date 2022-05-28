from config import CheckInSystemConfig
from db_table import db_table
from scanner import Scanner
from datetime import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger


class Checkpoints:
    def __init__(self, network, clockin = "9", clockout = "17"):
        self.config = CheckInSystemConfig(time(int(clockin)), time(int(clockout)))
        self.scheduler = BackgroundScheduler({
            'apscheduler.timezone': 'America/Los_Angeles',
        })
        self.scanner = Scanner(network)
        self.addTrigger()
        self.scheduler.print_jobs()
        self.scheduler.start()

    def addTrigger(self):
        temp_config1 = '0-' + str(self.config.clockinTime.hour) + '/' + str(self.config.NON_WORKING_TIME_INTERVAL)
        temp_config2 = str(self.config.clockoutTime.hour) + '-23/' + str(self.config.NON_WORKING_TIME_INTERVAL)
        self.scheduler.add_job(
            func = self.scanner.scan,
            trigger = OrTrigger([
                CronTrigger(
                    day_of_week = 'mon-fri',
                    hour = temp_config1
                ),
                CronTrigger(
                    day_of_week = 'mon-fri',
                    hour = temp_config2
                ),
            ]),
            id = "non_working_time",
            replace_existing = True
        )
        temp_config3 = str(self.config.clockinTime.hour) + '-' + str(self.config.clockoutTime.hour)
        temp_config4 = '*/' + str(self.config.WORKING_TIME_INTERVAL)
        self.scheduler.add_job(
            func = self.scanner.scan,
            trigger = CronTrigger(
                day_of_week = 'mon-fri',
                hour = temp_config3,
                minute = temp_config4
            ),
            id = "working_time",
            replace_existing = True
        )
        self.scheduler.add_job(
            func = self.scanner.scan,
            trigger = OrTrigger([
                CronTrigger(
                    day_of_week = 'mon-fri',
                    hour = self.config.clockinTime.hour - 1,
                    minute = str(60 - self.config.BEFORE_CLOCK) + '-59/' + str(self.config.WINDOW_INTERVAL)
                ),
                CronTrigger(
                    day_of_week = 'mon-fri',
                    hour = self.config.clockoutTime.hour - 1,
                    minute = str(60 - self.config.AFTER_CLOCK) + '-59/' + str(self.config.WINDOW_INTERVAL)
                ),
            ]),
            id = "before_window",
            replace_existing = True
        )
        self.scheduler.add_job(
            func = self.scanner.scan,
            trigger = OrTrigger([
                CronTrigger(
                    day_of_week = 'mon-fri',
                    hour = self.config.clockinTime.hour,
                    minute = '0-' + str(self.config.AFTER_CLOCK) + '/' + str(self.config.WINDOW_INTERVAL)
                ),
                CronTrigger(
                    day_of_week = 'mon-fri',
                    hour = self.config.clockoutTime.hour,
                    minute = '0-' + str(self.config.BEFORE_CLOCK) + '/' + str(self.config.WINDOW_INTERVAL)
                )
            ]),
            id = "after_window",
            replace_existing = True
        )