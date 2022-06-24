import scapy.all as scapy
from datetime import datetime, date, time
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

if __name__ == "__main__":
    scanner = Scanner()
    ipdict = scanner.scan()
    for data in ipdict.items():
        print(data)
    print(len(ipdict))
