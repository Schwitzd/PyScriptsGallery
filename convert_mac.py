import re
import argparse
import sys


def get_args():
    """Get all arguments"""
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
    """Remove special characters from MAC"""
    return re.sub('[-:.]', '', mac)


def validate_mac(mac):
    """Validate MAC Address"""
    if re.match(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', mac):
        return 'canonical'
    elif re.match(r'([0-9A-Fa-f]{4}[\.]){2}([0-9A-Fa-f]{4})', mac):
        return 'cisco'
    else:
        raise ValueError('Provided an invalid MAC Address')


def format_canonical_mac(mac):
    """Convert MAC into canonical format"""
    cleaned_mac = clean_mac(mac)
    mac = ':'.join(re.findall('.{2}', cleaned_mac))
    return mac


def format_cisco_mac(mac):
    """Convert MAC into Cisco format"""
    cleaned_mac = clean_mac(mac)
    mac = '.'.join(re.findall('.{4}', cleaned_mac))
    return mac


def main():
    """Script main function"""
    args = get_args()
    try:
        mac_format = validate_mac(args.macaddress)
    except ValueError as error:
        print(error)
        sys.exit(1)


    if mac_format == 'cisco':
        mac = format_canonical_mac(args.macaddress)
    elif mac_format == 'canonical':
        mac = format_cisco_mac(args.macaddress)

    print(mac)


if __name__ == "__main__":
    main()
