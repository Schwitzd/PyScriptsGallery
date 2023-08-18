import argparse
from typing import List
from scapy.all import srp, Ether, ARP
from tabulate import tabulate


def get_arguments() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target',
                        help='Target IP or IP Range')
    arguments = parser.parse_args()

    return arguments


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
