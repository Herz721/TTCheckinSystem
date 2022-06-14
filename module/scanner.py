import scapy.all as scapy
from datetime import datetime, date
import subprocess
from db_table import Employee, ClockRecord, Device
import socket

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
        answered_list = scapy.srp(arp_request_broadcast, timeout = 1, retry = 10, verbose = False)[0]

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
        reportFile = open("../daily_reports/" + todayDate + ".txt", "w")
        reportList = queryall()
        # report[0]: name; report[1]: date; report[2]: onboard_time
        for report in reportList:
            reportFile.write("user_name: " + report[0] + "\n")
            reportFile.write("date: " + report[1] + "\n")
            reportFile.write("onboard time: " + report[2] + "\n")
            reportFile.write("----------------------------------------\n")
        reportFile.close()

    def queryall(self):
        res = []
        todayDate = str(date.today())
        employeeList = self.db.session.query(Employee).all()
        for employee in employeeList:
            res.append((employee.ename, todayDate, self.query(employee.eid, todayDate)))
        return res

    def query(self, eid, date):
        res = ""
        status = 0
        results = self.db.session.query(ClockRecord).filter_by(eid = eid, rdate = date).all()
        for result in results:
            if status == 0 and result.status == 1:
                begin_time = str(result.check_point)
                res = res + begin_time + "-"
                status = 1
            if status == 1 and result.status == 0:
                end_time = str(result.check_point)
                res = res + end_time + "; "
                status = 0
        return res



if __name__ == "__main__":
    scanner = Scanner()
    ipdict = scanner.scan()
    for data in ipdict.items():
        print(data)
    print(len(ipdict))
