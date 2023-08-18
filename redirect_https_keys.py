import os
import argparse


def get_args() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True,
                        dest='path', help='HTTPS keys file')
    args = parser.parse_args()

    return args

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
