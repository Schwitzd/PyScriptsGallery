"""
version: 1.1 | Author: Daniel Schwitzgebel | Created: 18.08.2023 | Updated: 20.04.2024
Description: This script checks the version of a given UUID and prints the result.

UUIDv1: Generated from timestamp and MAC address for time-based ordering.
UUIDv2: Similar to v1 with additional DCE security version component.
UUIDv3: Hashed from name and namespace using MD5 for specific naming.
UUIDv4: Completely random UUID for general-purpose uniqueness.
UUIDv5: Hashed from name and namespace using SHA-1 for stronger security.
"""

import uuid
import argparse


def check_uuid_version(input_uuid: str) -> int:
    """Check the version of a UUID"""
    try:
        uuid_obj = uuid.UUID(input_uuid)
        version = uuid_obj.version
        return version
    except ValueError:
        return -1


def get_args() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--uuid', type=str, required=True,
        help='The UUID to check'
    )

    return parser.parse_args()


def main():
    """Script main function"""
    args = get_args()
    version = check_uuid_version(args.uuid)

    if version == -1:
        print('Invalid UUID format')
    else:
        print(f'The UUID version is: {version}')


if __name__ == '__main__':
    main()
