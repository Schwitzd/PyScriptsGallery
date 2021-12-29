# 0011.2233.4455

import re
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-M', '--mac-address',
                        dest='macaddress',
                        help='type the Mac Address')

    args = parser.parse_args()

    if not args.macaddress:
        parser.error(
            "[-] Please specify a MAC Address, use --help for more info.")

    return args


def clean_mac(mac):
    return re.sub('[-:.]', '', mac)


def validate_mac(mac):
    if re.match(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', mac):
        return 'canonical'
    elif re.match(r'([0-9A-Fa-f]{4}[\.]){2}([0-9A-Fa-f]{4})', mac):
        return 'cisco'


def format_canonical_mac(mac):
    cleaned_mac = clean_mac(mac)
    mac = ':'.join(re.findall('.{2}', cleaned_mac))
    return mac


def format_cisco_mac(mac):
    cleaned_mac = clean_mac(mac)
    # assert mac.isalnum(), 'expected only alphanumeric charapters'
    mac = '.'.join(re.findall('.{4}', cleaned_mac))
    return mac


def main():
    args = get_arguments()
    mac_format = validate_mac(args.macaddress)
    if mac_format == 'cisco':
        mac = format_canonical_mac(args.macaddress)
    elif mac_format == 'canonical':
        mac = format_cisco_mac(args.macaddress)

    print(mac)


if __name__ == "__main__":
    main()
