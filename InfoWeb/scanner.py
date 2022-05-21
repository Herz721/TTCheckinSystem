import scapy.all as scapy
import time
import subprocess
from db_table import db_table

class Scanner():
    def __init__(self, network = "10.0.0.61/24", checkpoint = 0):
        self.network = network
        self.checkpoint = checkpoint  # seconds

    def scan(self):
        macdict = {}
        arp_request = scapy.ARP(pdst = self.network)
        broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        # src = mac address; psrc = ip address; dst = local mac address; pdst = local ip address
        for host in answered_list:
            if host[1].src not in macdict.keys():
                macdict[host[1].src] = host[1].psrc
        db = db_table()
        db.select("SELECT * FROM EMPLOYEE")
        db.close()
        return macdict


if __name__ == "__main__":
    scanner = Scanner()
    macdict = scanner.scan()
    for mac in macdict:
        print(mac)