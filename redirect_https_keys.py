"""
version: 1.4 | Author: Daniel Schwitzgebel | Created: 18.08.2023 | Updated: 20.04.2024
Description: This script creates a key file for HTTPS decryption and sets the SSLKEYLOGFILE environment variable accordingly.
"""

import os
import argparse


def get_args() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--path', required=True, dest='path',
        help='HTTPS keys file'
    )

    return parser.parse_args()

def main():
    """Create the key file and add the env variable"""
    args = get_args()
    keylog_path = args.path
    keylog_file = os.path.join(keylog_path, 'keylog.txt')

    if not os.path.exists(keylog_path):
        os.makedirs(keylog_path)

    with open(keylog_file, 'w', encoding='utf-8'):
        pass

    os.environ['SSLKEYLOGFILE'] = keylog_path


if __name__ == '__main__':
    main()
