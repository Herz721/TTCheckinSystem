import scapy.all as scapy
import time
import subprocess
from db_table import db_table

class Scanner():
    def __init__(self, network = "10.0.0.61/24"):
        self.network = network
        self.time = interval  # seconds



    def scan(self):
        macList = set()
        arp_request = scapy.ARP(pdst = self.network)
        broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        # src = mac address; psrc = ip address; dst = local mac address; pdst = local ip address
        for host in answered_list:
            macList.add(host[1].psrc)



def main():
    scanner = Scanner()
    scanner.scan()


if __name__ == "__main__":
    main()