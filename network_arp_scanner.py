"""
version: 2.2 | Author: Daniel Schwitzgebel | Created: 31.01.2022 | Updated: 20.04.2024
Description: This script scans for active devices on a network using ARP and displays their IP and MAC addresses.
"""

import argparse
from typing import List
from scapy.all import srp, Ether, ARP
from tabulate import tabulate


def get_arguments() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--target', dest='target',
        help='Target IP or IP Range'
    )

    return parser.parse_args()


def arp_scan(ip: str) -> List[str]:
    """Scan ip subnet"""
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_awake = []
    for response in answered_list:
        client_response = [response[1].psrc, response[1].hwsrc]
        clients_awake.append(client_response)

    return clients_awake


def print_result(results_list: List[str]) -> str:
    """Print results"""
    headers = ['IP', 'MAC Address']
    print()
    print(tabulate(results_list, headers=headers, tablefmt='simple'))


if __name__ == '__main__':
    args = get_arguments()
    scan_result = arp_scan(args.target)
    if scan_result:
        print_result(scan_result)
