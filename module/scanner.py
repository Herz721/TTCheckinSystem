import scapy.all as scapy
from datetime import datetime, date
import subprocess
from db_table import EMPLOYEE, CLOCKRECORD

class Scanner():
    def __init__(self, db, network = "192.168.0.63"):
        self.network = network + "/24"
        self.db = db
        print(self.network)

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
        ipResults = self.db.session.query(EMPLOYEE).all()
        self.insertRecord(ipResults, ipdict, date.today())

    def insertRecord(self, ipResults, ipdict, date):
        """
        Insert checkpoints records

        Args:
            ipResults (list): all employee records in database
            ipdict (dict): (ip:mac) dict
            date (date): today date
        """
        checkpoint = datetime.now().strftime("%H:%M")
        for result in ipResults:
            if result.MAC in ipdict.values():
                vals = CLOCKRECORD(result.EID, checkpoint, date, 1)
            else:
                vals = CLOCKRECORD(result.EID, checkpoint, date, 0)
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