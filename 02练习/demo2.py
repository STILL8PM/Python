from concurrent.futures import ThreadPoolExecutor
import _thread
import struct
import time
import os
import re
import socket
import pandas as pd


def calc_checksum(src_bytes):
    """用于计算ICMP报文的校验和"""
    total = 0
    max_count = len(src_bytes)
    count = 0
    while count < max_count:
        val = src_bytes[count + 1]*256 + src_bytes[count]
        total = total + val
        total = total & 0xffffffff
        count = count + 2

    if max_count < len(src_bytes):
        total = total + ord(src_bytes[len(src_bytes) - 1])
        total = total & 0xffffffff

    total = (total >> 16) + (total & 0xffff)
    total = total + (total >> 16)
    answer = ~total
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return socket.htons(answer)


def sent_ping(icmp_socket, target_addr, identifier=os.getpid() & 0xFFFF,
              serial_num=0, data=None):
    # 校验需要后面再计算，这里先设置为0
    ICMP_ECHO_REQUEST, code, checksum = 8, 0, 0
    # 初步打包ICMP头部
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, code,
                         checksum, identifier, serial_num)
    # 打包选项数据
    if data:
        data = data.ljust(192, b"Q")
    else:
        data = struct.pack("d", time.time()).ljust(192, b"Q")
    checksum = calc_checksum(header + data)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, code,
                         checksum, identifier, serial_num)
    # 发送给目标地址，ICMP协议没有端口的概念端口可以随便填
    icmp_socket.sendto(header + data, (target_addr, 1))


def receive_pong(icmp_socket, net_segment, timeout=2):
    icmp_socket.settimeout(timeout)
    ips = set()
    while True:
        start_time = time.time()
        try:
            recv_packet, (ip, port) = icmp_socket.recvfrom(1024)
            if ip.startswith(net_segment):
                ips.add(ip)
        except socket.timeout as e:
            break
    return ips


def ping_net_segment_all(icmp_socket, net_segment):
    for i in range(1, 255):
        ip = f"{net_segment}.{i}"
        sent_ping(icmp_socket, ip)


last = None
while 1:
    icmp_socket = socket.socket(
        socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    with ThreadPoolExecutor() as p:
        p.submit(ping_net_segment_all, icmp_socket, "192.168.2")
        future = p.submit(receive_pong, icmp_socket, "192.168.2")
        ips = future.result()
    if last is None:
        print("当前在线设备：", ips)
    if last:
        up = ips-last
        if up:
            print("\r新上线设备：", up, end=" "*100)
        down = last-ips
        if down:
            print("\r刚下线设备：", down, end=" "*100)
    last = ips
    time.sleep(3)
