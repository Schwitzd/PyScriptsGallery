
import argparse
import subprocess
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt
from scapy.packet import Packet
from scapy.sendrecv import sniff
from tabulate import tabulate
from typing import List, Tuple, Set

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Check Access Points enforcing PMF')
    parser.add_argument('-I', '--interface', dest='interface', type=str, help='WiFi interface name')
    parser.add_argument('--timeout', dest='timeout', type=int, default=10, help='Capture timeout in seconds (default: 10)')
    return parser.parse_args()

def check_interface_monitor_mode(interface: str) -> None:
    """Check if the interface is in monitoring mode"""
    try:
        iwconfig_output = subprocess.check_output(['iwconfig', interface], stderr=subprocess.STDOUT, universal_newlines=True)
        if 'Mode:Monitor' not in iwconfig_output:
            raise ValueError(f"Interface '{interface}' is not in monitoring mode.")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Error checking interface '{interface}' mode: {e.output.strip()}") from e

def check_pmf_for_aps(interface: str) -> List[Tuple[str, str, str]]:
    aps_info: List[Tuple[str, str, str]] = []
    discovered_aps: Set[str] = set()

    def packet_handler(pkt: Packet) -> None:
        if pkt.haslayer(Dot11) and pkt.type == 0 and pkt.subtype == 8:
            ap_mac = pkt[Dot11].addr3
            ssid = pkt[Dot11Elt].info.decode('utf-8')
            pmf_flag = (pkt[Dot11Beacon].cap & 0x0010) != 0

            ap_key = f'{ap_mac}:{ssid}'
            if ap_key not in discovered_aps:
                discovered_aps.add(ap_key)
                aps_info.append((ap_mac, ssid, 'Yes' if pmf_flag else 'No'))

    sniff(iface=interface, prn=packet_handler)

    return aps_info

def main() -> None:
    args = parse_args()

    try:
        check_interface_monitor_mode(args.interface)  # Check if the interface is in monitor mode
        ap_info = check_pmf_for_aps(args.interface)

        if ap_info:
            print(tabulate(ap_info, headers=['BSSID', 'SSID', 'PMF Enabled'], tablefmt='grid'))
        else:
            print('No Access Points found in the capture')
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
