import ssl
import socket
import argparse


def get_arguments() -> argparse.Namespace:
    """Parse the command-line arguments"""

    parser = argparse.ArgumentParser(description='Get Subject Alternative Names (SANs) for a website.')
    parser.add_argument('--website', type=str, help='The website domain.')
    parser.add_argument('--port', type=int, default=443, help='The port to connect to. Default is 443.')

    args = parser.parse_args()

    return args


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

    san_list = get_san_list(args.website, args.port)

    print('Subject Alternative Names (SANs) for:', args.website)
    for san in san_list:
        print(san)


if __name__ == '__main__':
    main()
