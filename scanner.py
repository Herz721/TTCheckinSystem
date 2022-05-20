import scapy.all as scapy
import time
import subprocess

class Scanner():
    def __init__(self, network = "10.0.0.61/24", interval = 30):
        self.network = network
        self.interval = interval  # seconds


    def scan(self):
        macList = set()
        arp_request = scapy.ARP(pdst = self.network)
        broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        # src = mac address; psrc = ip address; dst = local mac address; pdst = local ip address
        for host in answered_list:
            macList.add(host[1].src)
        return macList

    def connection_change(hosts, action):
        if action not in ("connected", "disconnected"):
            raise ValueError(f"Invalid action: {action}")
        for host in hosts:
            device = dictionary[host] if host in dictionary else 'unknown device'
            if action == 'connected':
                say = f"echo {device} connected | cscript C:\\Progra~1\\Jampal\\ptts.vbs"
            else:
                say = f"echo {device} disconnected | cscript C:\\Progra~1\\Jampal\\ptts.vbs"
            subprocess.call(say, shell=True, stdout=None, stderr=None)


def main():
    scanner = Scanner()
    old_macs = scanner.scan()
    for mac in old_macs:
        print(mac)
    # connection_change(old_macs, "connected")
    # while True:
    #     time.sleep(INTERVAL)
    #     macs = scan(NETWORK)

    #     new = macs - old_macs
    #     connection_change(new, "connected")

    #     left = old_macs - macs
    #     connection_change(left, "disconnected")

    #     old_macs = macs


if __name__ == "__main__":
    main()