"""
version: 1.4 | Author: Daniel Schwitzgebel | Created: 08.06.2022 | Updated: 20.04.2024
Description: This script unshortens a given URL, resolving any redirects, and returns the original URL.
"""

import argparse
import requests


def get_arguments() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest='url', help='URL to unshort')

    return parser.parse_args()


def unshorten_url(url: str) -> str:
    """Unshort the URL"""
    try:
        session = requests.Session()
        response = session.head(url, allow_redirects=True)
        return response.url
    except requests.exceptions.RequestException as error:
        return f'Error occurred while unshortering URL: {error}'


if __name__ == '__main__':
    args = get_arguments()
    ori_url = unshorten_url(args.url)
    print (ori_url)
