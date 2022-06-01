import scapy.all as scapy
from datetime import datetime, date
import subprocess
from db_table import db_table

class Scanner():
    def __init__(self, network = "192.168.0.63"):
        self.network = network + "/24"
        print(self.network)

    def findIpDict(self):
        ipdict = {}
        arp_request = scapy.ARP(pdst = self.network)
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
        db = db_table()
        ipResults = db.select("SELECT MAC, EID FROM EMPLOYEE")
        self.insertRecord(ipResults, ipdict, date.today())
        db.close()

    def insertRecord(self, ipResults, ipdict, date):
        checkpoint = datetime.now().strftime("%H:%M")
        for result in ipResults:
            if result[0] in ipdict.values():
                vals = (result[1], checkpoint, date, 1)
            else:
                vals = (result[1], checkpoint, date, 0)
            db = db_table()
            sql = "INSERT INTO CLOCKRECORDS (EID, CHECKPOINT, RDATE, STATUS) VALUES (%s, %s, %s, %s);"
            db.insert(sql, vals)
            db.close()


if __name__ == "__main__":
    scanner = Scanner()
    ipdict = scanner.scan()
    for data in ipdict.items():
        print(data)
    print(len(ipdict))