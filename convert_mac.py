import os
import sys
import subprocess
import codecs
import argparse
from scapy.all import sniff, RadioTap, Dot11, Dot11ProbeResp, Dot11ProbeReq, Dot11Beacon, Dot11Elt


def get_args() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--interface', dest='interface', help='Specify the WiFi interface in monitoring mode')

    args = parser.parse_args()

    if not args.interface:
        parser.error('[-] Please specify a WiFi interface.')

    return args


def check_interface_monitor_mode(interface: str) -> None:
    """Check if the interface is in monitoring mode"""
    try:
        iwconfig_output = subprocess.check_output(['iwconfig', interface], stderr=subprocess.STDOUT, universal_newlines=True)
        if "Mode:Monitor" not in iwconfig_output:
            raise ValueError(f"Interface '{interface}' is not in monitoring mode.")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Error checking interface '{interface}' mode: {e.output.strip()}") from e


def handler(p):
    if not (p.haslayer(Dot11ProbeResp) or p.haslayer(Dot11ProbeReq) or p.haslayer(Dot11Beacon)):
        return

    radio_tap = p.getlayer(RadioTap)
    dot11_layer = p.getlayer(Dot11)

    rssi = radio_tap.dBm_AntSignal
    dst_mac = dot11_layer.addr1
    src_mac = dot11_layer.addr2
    ap_mac = dot11_layer.addr3
    info = f'rssi={rssi:2}dBm, dst={dst_mac}, src={src_mac}, ap={ap_mac}'

    if p.haslayer(Dot11ProbeResp):
        ssid = codecs.decode(dot11_layer.info, "utf-8")
        channel = ord(p[Dot11Elt:3].info)
        print(f'[ProbResp] {info}, chan={channel}, ssid=\"{ssid}\"')
    elif p.haslayer(Dot11ProbeReq):
        print(f'[ProbReq ] {info}')
    elif p.haslayer(Dot11Beacon):
        ssid = dot11_layer.info.decode('utf-8')
        channel = ord(p[Dot11Elt:3].info)
        interval = dot11_layer.beacon_interval
        print(f'[Beacon  ] {info}, chan={channel}, interval={interval}, ssid=\"{ssid}\"')


def main():
    """Script main function"""
    args = get_args()

    try:
        check_interface_monitor_mode(args.interface)
        sniff(iface=args.interface, prn=handler, store=0)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[+] Sniffing stopped by user.")


if __name__ == '__main__':
    main()
