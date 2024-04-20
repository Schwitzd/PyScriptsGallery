"""
version: 1.4 | Author: Daniel Schwitzgebel | Created: 31.01.2022 | Updated: 20.04.2024
Description: This script scans a specified subnet for active hosts and displays their IP addresses.
"""

import argparse
import ipaddress
from scapy.all import sr, IP, ICMP


def get_arguments()-> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--subnet', type=str,
        help='An IP address in CIDR notation defining a subnet to scan.'
    )

    parser.add_argument(
        '--activeonly', action='store_true',
        help='Show only active hosts.'
    )

    return parser.parse_args()


def scan(netmask: str) -> str:
    """Scan subnet"""
    for ip_addr in ipaddress.IPv4Network(netmask):
        ip_request = IP(dst=str(ip_addr))
        ans, unans = sr(ip_request / ICMP(), timeout=2, verbose=0)

        if not unans:
            ans.summary(
                lambda p: p[1].sprintf(f'[+] {IP.src}: is UP')
            )
        elif args.activeonly is None:
            print(f'[-] {ip_addr}: is DOWN')


if __name__ == '__main__':
    args = get_arguments()
    scan(args.subnet)
