#!/usr/bin/env python

import argparse
import socket
import ipaddress
import bannergrab
from concurrent.futures import ThreadPoolExecutor

# Define the list of important ports
IMPORTANT_PORTS = [20, 21, 22, 23, 25, 53, 69, 80, 110, 143, 587, 2082, 2484, 3306, 5432]

def scan_host(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((str(ip), port))
        if result == 0:
            banner = bannergrab.grab_banner(ip, port)
            print(f"Port {port} is open on {ip}")
            print(f"Service: {banner}")
        sock.close()
    except socket.error:
        pass

def network_scan(targets, ports=None, scan_technique='connect', important_ports=False):
    with ThreadPoolExecutor(max_workers=100) as executor:
        if ports is None:
            if important_ports:
                ports = IMPORTANT_PORTS
            else:
                ports = range(1, 1025)  # Default range set to scan ports 1-1024
        elif isinstance(ports, int):
            ports = [ports]
        for target in targets:
            ip_net = ipaddress.ip_network(target)
            if ip_net.num_addresses == 1:  # Single IP address
                for port in ports:
                    executor.submit(scan_host, target, port)
            else:  # IP range
                for ip in ip_net.hosts():
                    for port in ports:
                        executor.submit(scan_host, ip, port)

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Python Network Scanner')
    parser.add_argument('targets', nargs='+', help='IP address(es) or IP range(s) to scan')
    parser.add_argument('-p', '--ports', type=int, nargs='*', help='Ports to scan (default: 1-1024)')
    parser.add_argument('-t', '--technique', choices=['connect', 'syn', 'udp'], default='connect',
                        help='Scan technique to use (default: connect)')
    parser.add_argument('--imp', action='store_true', help='Scan important ports')
    args = parser.parse_args()

    # Perform network scanning
    network_scan(args.targets, args.ports, args.technique, args.imp)
