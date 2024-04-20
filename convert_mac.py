"""
version: 2.4 | Author: Daniel Schwitzgebel | Created: 29.12.2021 | Updated: 20.04.2024
Description: This script retrieves the Subject Alternative Names (SANs) for a given website domain.
"""

import re
import argparse


def get_args() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-M', '--mac-address', dest='macaddress',
        help='type the Mac Address'
    )

    args = parser.parse_args()

    if not args.macaddress:
        parser.error(
            '[-] Please specify a MAC Address, use --help for more info.')

    return args


class MacAddress():
    """This class manypulate the MAC address format"""
    def __init__(self, mac: str) -> None:
        self.mac_cleaned = self._clean_mac(mac)
        self.format = self._validate_mac(mac)

    def _clean_mac(self, mac: str) -> str:
        return re.sub('[-:.]', '', mac)

    def _validate_mac(self, mac):
        if re.match(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', mac):
            return 'canonical'
        elif re.match(r'([0-9A-Fa-f]{4}[\.]){2}([0-9A-Fa-f]{4})', mac):
            return 'cisco'
        else:
            raise ValueError('Provided an invalid MAC Address')

    def to_canonical(self) -> str:
        """Convert MAC into canonical format"""
        return ':'.join(re.findall('.{2}', self.mac_cleaned))

    def to_cisco(self) -> str:
        """Convert MAC into Cisco format"""
        return '.'.join(re.findall('.{4}', self.mac_cleaned))


def main():
    """Script main function"""
    args = get_args()
    mac = MacAddress(args.macaddress)
    if mac.format == 'cisco':
        print(mac.to_canonical())
    elif mac.format == 'canonical':
        print(mac.to_cisco())


if __name__ == '__main__':
    main()
