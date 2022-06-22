import scapy.all as scapy
from datetime import datetime, date, time
import subprocess
from db_table import Employee, ClockRecord, Device
import socket
from config import CheckInSystemConfig, EmailConfig
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Scanner():
    def __init__(self, db):
        self.network = self.get_ip() + "/24"
        self.db = db
        print(self.network)

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def findIpDict(self):
        """
        Find dict[ip:mac] by ARPing

        Returns:
            [dict]: [key: ip address; value: mac address]
        """
        ipdict = {}
        arp_request = scapy.ARP(pdst = self.network)
        # broadcast
        broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout = 1, retry = 5, verbose = False)[0]

        # src = mac address; psrc = ip address; dst = local mac address; pdst = local ip address
        for host in answered_list:
            ipdict[host[1].psrc] = host[1].src
        return ipdict

    def scan(self):
        ipdict = self.findIpDict()
        # insert checkpoints
        employeeList = self.db.session.query(Employee).all()
        print(ipdict)
        self.insertRecord(employeeList, ipdict, date.today())

    def insertRecord(self, employeeList, ipdict, date):
        """
        Insert checkpoints records

        Args:
            employeeList (list): all employee records in database
            ipdict (dict): (ip:mac) dict
            date (date): today date
        """
        checkpoint = datetime.now().strftime("%H:%M")
        for employee in employeeList:
            devices = self.db.session.query(Device).filter_by(dev_type = "phone", eid = employee.eid)
            isHere = False
            for device in devices:
                if device.MAC in ipdict.values():
                    vals = ClockRecord(employee.eid, checkpoint, date, 1)
                    isHere = True
                    break
            if not isHere:
                vals = ClockRecord(employee.eid, checkpoint, date, 0)
            self.db.session.add(vals)
            self.db.session.commit()
            self.db.session.flush()
        print(checkpoint + ": insert Successfully!")

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
        message['To'] = receiver_address
        message['Subject'] = todayDate + '\'s Clockin Report'
        #The body and the attachments for the mail
        message.attach(MIMEText(content, 'plain'))
        #Create SMTP session for sending the mail
        # try:
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent!')
        # except smtplib.SMTPException:
        #     print ("Error: Mail Sent Failure")


    

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



if __name__ == "__main__":
    scanner = Scanner()
    ipdict = scanner.scan()
    for data in ipdict.items():
        print(data)
    print(len(ipdict))
