# 检测本机所在局域网内网络流量和数据包收发情况
## 需要将网上设置为混杂模式
## https://www.mingrisoft.com/Books/bookType1/bid/543/cid/17.html

import socket
import os
import struct
import ctypes

host = "192.168.43.235"


class IP(ctypes.Structure):
    _fields_ = [
        ("ihl", ctypes.c_ubyte, 4),
        ("version", ctypes.c_ubyte, 4),
        ("tos", ctypes.c_ubyte),
        ("len", ctypes.c_ushort),
        ("id", ctypes.c_ushort),
        ("offset", ctypes.c_ubyte),
        ("ttl", ctypes.c_ubyte),
        ("protocol_num", ctypes.c_ubyte),
        ("sum", ctypes.c_ushort),
        ("src", ctypes.c_ulong),
        ("dst", ctypes.c_ulong)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self):
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


if os.name == "nt":
    # win 平台
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host, 0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == "nt":
    # WIN平台上，需要设置IOCTL以启用混杂模式
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        raw_buffer = sniffer.recvfrom(65565)[0]
        ip_header = IP(raw_buffer[0:20])
        print("Protocol:{}{}->{}".format(ip_header.protocol, ip_header.src_address, ip_header.dst_address))
except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
