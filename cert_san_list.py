"""
version: 1.2 | Author: Daniel Schwitzgebel | Created: 21.12.2023 | Updated: 20.04.2024
Description: This script manipulates MAC addresses between Cisco and canonical formats.
"""

import ssl
import socket
import argparse


def get_arguments() -> argparse.Namespace:
    """Parse the command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Get Subject Alternative Names (SANs) for a website.'
    )
    parser.add_argument(
        '--url', type=str,
        help='The website domain.'
    )
    parser.add_argument(
        '--port', type=int, default=443,
        help='The port to connect to. Default is 443.'
    )

    return parser.parse_args()


def get_san_list(domain: str, port: int) -> list[str]:
    """Retrieve the Subject Alternative Names (SANs) for a given website domain"""
    context = ssl.create_default_context()
    with socket.create_connection((domain, port)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
            san_list = []
            for _, value in cert.get('subjectAltName', []):
                san_list.append(value)
            
            return san_list


def main():
    args = get_arguments()

    san_list = get_san_list(args.url, args.port)
    print('Subject Alternative Names (SANs) for:', args.website)
    for san in san_list:
        print(san)


if __name__ == '__main__':
    main()
