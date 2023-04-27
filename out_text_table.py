import argparse
from prettytable import from_csv


def get_args() -> argparse.Namespace:
    '''Define the input arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--csvfile',
                        dest='csvfile',
                        type=argparse.FileType('r'),
                        help='CSV file path')

    arguments = parser.parse_args()

    if not arguments.csvfile:
        parser.error(
            '[-] Please specify a csv file, use --help for more info.')

    return arguments


def main():
    '''Main function'''
    args = get_args()
    with args.csvfile as csvfile:
        output = from_csv(csvfile)

    print(output)


if __name__ == '__main__':
    main()
