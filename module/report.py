import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, date, time
from config import CheckInSystemConfig, EmailConfig
from db_table import Employee, ClockRecord, Device

class ReportFunc():
    def __init__(self, db):
        self.db = db

    def create_DailyReport(self):
        todayDate = str(date.today())
        with open("../daily_reports/" + todayDate + ".txt", "w") as reportFile:
            reportFile.seek(0)
            reportFile.truncate()
            reportList = self.queryall(todayDate)
            # report[0]: name; report[1]: date; report[2]: onboard_time
            reportStr = str()
            for report in reportList:
                reportStr = reportStr + "user_name: " + report[0] + "\n"
                reportStr = reportStr + "date: " + report[1] + "\n"
                reportStr = reportStr + "onboard time: " + report[2] + "\n"
                reportStr = reportStr + "----------------------------------------\n"
            reportFile.write(reportStr)
            reportFile.close()
            print("Write Successfully!")
        self.send_email(reportStr, todayDate)

    def send_email(self, content, todayDate):
        #The mail addresses and password
        sender_address = EmailConfig.SENDER_ADDR
        sender_pass = EmailConfig.SENDER_PWD
        receiver_address = EmailConfig.RECEIVER_ADDR
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = ", ".join(receiver_address)
        message['Subject'] = todayDate + '\'s Clockin Report'
        #The body and the attachments for the mail
        message.attach(MIMEText(content, 'plain'))
        #Create SMTP session for sending the mail
        try:
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(sender_address, sender_pass) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            print('Mail Sent!')
        except smtplib.SMTPException:
            print ("Error: Mail Sent Failure")

    def queryall(self, todayDate = str(date.today())):
        res = []
        employeeList = self.db.session.query(Employee).filter_by(status = "onsite").all()
        for employee in employeeList:
            res.append((employee.ename, todayDate, self.query(employee.eid, todayDate)))
        return res

    def query(self, eid, date):
        res = ""
        status = 0
        results = self.db.session.query(ClockRecord).filter_by(eid = eid, rdate = date).all()
        begin_time = time()
        end_time = time()
        # status: 1 = clockin; 2 = absent?; 0 = clockout
        for result in results:
            if status == 0 and result.status == 1:
                begin_time = result.check_point
                res = res + str(begin_time) + "-"
                status = 1
            if status == 1 and result.status == 0:
                leave_time = result.check_point
                status = 2
            if status == 2 and result.status == 0:
                end_time = result.check_point
                interval =  (end_time.hour - leave_time.hour) * 60 + end_time.minute - leave_time.minute
                if interval > CheckInSystemConfig.REPORT_ALLOWANCE_INTERVAL:
                    res = res + str(leave_time) + "; "
                    status = 0
            if status == 2 and result.status == 1:
                status = 1
        return res
