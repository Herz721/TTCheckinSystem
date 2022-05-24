from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(func = , trigger = "cron", day_of_week = "mon-fri", hour = 8)
sched.start()
