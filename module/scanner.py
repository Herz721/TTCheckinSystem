import scapy.all as scapy
from datetime import datetime, date
import subprocess
from db_table import db_table

class Scanner():
    def __init__(self, network = "10.0.0.61/24"):
        self.network = network

    def scan(self):
        ipdict = {}
        arp_request = scapy.ARP(pdst = self.network)
        broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout = 1, retry = 5, verbose = False)[0]

        # src = mac address; psrc = ip address; dst = local mac address; pdst = local ip address
        for host in answered_list:
            ipdict[host[1].psrc] = host[1].src

        # update mac address
        db = db_table()
        results = db.select("SELECT IP, MAC, EID FROM EMPLOYEE")
        self.updateMac(results, ipdict)
        self.insertRecord(results, ipdict, date.today())
        db.close()

        return ipdict

    def updateMac(self, ipResults, ipdict):
        for result in ipResults:
            if result[0] in ipdict.keys():
                if result[1] is None:
                    db = db_table()
                    sql = "UPDATE EMPLOYEE SET MAC = %s WHERE ip = %s"
                    vals = (ipdict[result[0]], result[0])
                    db.update(sql, vals)
                    db.close()
                elif result[1] == ipdict[result[0]]:
                    print("%s: MAC Address Already Exists" % result[0])
                else:
                    print("Conflict on MAC Address!")
                    # TODO

    def insertRecord(self, ipResults, ipdict, date):
        checkpoint = datetime.now().strftime("%H:%M")
        for result in ipResults:
            if result[0] in ipdict.keys():
                vals = (result[2], checkpoint, date, 1)
            else:
                vals = (result[2], checkpoint, date, 0)
            db = db_table()
            sql = "INSERT INTO CLOCKRECORDS (EID, CHECKPOINT, RDATE, STATUS) VALUES (%s, %s, %s, %s);"
            db.insert(sql, vals)
            db.close()


if __name__ == "__main__":
    scanner = Scanner()
    ipdict = scanner.scan()
    for data in ipdict.items():
        print(data)