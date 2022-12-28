import argparse
import requests


def get_arguments():
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest='url', help='URL to unshort')
    args = parser.parse_args()
    return args


def unshorten_url(url):
    """Unshort the URL"""
    try:
        session = requests.Session()
        response = session.head(url, allow_redirects=True)
        print(response.url)
    except Exception as error:
        print(error)


if __name__ == '__main__':
    args = get_arguments()
    unshorten_url(args.url)
