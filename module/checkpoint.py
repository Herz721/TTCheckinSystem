from config import CheckInSystemConfig
from db_table import db_table
from scanner import Scanner
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

class Checkpoints:
    def __init__(self):
        self.config = CheckInSystemConfig()
        self.scheduler = BackgroundScheduler({
            'apscheduler.timezone': 'America/Los_Angeles',
        })
        self.scanner = Scanner()
        self.addTrigger()

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
        temp_config5 = str(60 - self.config.BEFORE_CLOCK) + '-59/' + str(self.config.WINDOW_INTERVAL)
        self.scheduler.add_job(
            func = self.scanner.scan,
            trigger = OrTrigger([
                CronTrigger(
                    day_of_week = 'mon-fri',
                    hour = self.config.clockinTime.hour - 1,
                    minute = temp_config5
                ),
                CronTrigger(
                    day_of_week = 'mon-fri',
                    hour = self.config.clockoutTime.hour - 1,
                    minute = temp_config5
                ),
            ]),
            id = "before_window",
            replace_existing = True
        )
        temp_config6 = '0-' + str(self.config.AFTER_CLOCK - 1) + '/' + str(self.config.WINDOW_INTERVAL)
        self.scheduler.add_job(
            func = self.scanner.scan,
            trigger = OrTrigger([
                CronTrigger(
                    day_of_week = 'mon-fri',
                    hour = self.config.clockinTime.hour,
                    minute = temp_config6
                ),
                CronTrigger(
                    day_of_week = 'mon-fri',
                    hour = self.config.clockoutTime.hour,
                    minute = temp_config6
                )
            ]),
            id = "after_window",
            replace_existing = True
        )