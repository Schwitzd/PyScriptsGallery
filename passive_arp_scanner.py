import argparse
import os
from scapy.all import ARP, sniff

discovered_devices = {}


def arp_scanner_callback(pkt: ARP) -> None:
    """
    Callback function to process ARP packets and discover devices on the network.
    """
    global discovered_devices
    if ARP in pkt and pkt[ARP].op in (1, 2):  # ARP who-has or is-at
        mac_address = pkt[ARP].hwsrc
        ip_address = pkt[ARP].psrc
        if mac_address not in discovered_devices:
            discovered_devices[mac_address] = ip_address
            print(f"IP: {ip_address} - MAC: {mac_address}")


def check_interface_exists(interface: str) -> bool:
    """
    Check if the specified network interface exists.
    """
    available_interfaces = os.listdir('/sys/class/net')
    return interface in available_interfaces


def passive_arp_scanner(interface: str) -> None:
    """
    Start the passive ARP scanner on the specified interface.
    """
    if not check_interface_exists(interface):
        print(f"Error: Interface '{interface}' does not exist.")
        return

    print(f'Passive ARP Scanner started on interface {interface}. Press Ctrl+C to stop.\n')
    try:
        sniff(filter="arp", prn=arp_scanner_callback, iface=interface, store=0)
    except KeyboardInterrupt:
        print('Passive ARP Scanner stopped.')


def get_args() -> argparse.Namespace:
    """
    Get command-line arguments using argparse.
    """
    parser = argparse.ArgumentParser(description='Passive ARP Scanner')
    parser.add_argument('-i', '--interface', required=True, help='Interface to monitor')
    return parser.parse_args()


def main() -> None:
    """
    Main function to run the ARP scanner.
    """
    args = get_args()
    try:
        passive_arp_scanner(args.interface)
    except ValueError as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
