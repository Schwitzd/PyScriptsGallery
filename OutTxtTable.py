import argparse
from prettytable import from_csv

parser = argparse.ArgumentParser()
parser.add_argument('--csvfile', type=argparse.FileType('r'), help="CSV file path")
args = parser.parse_args()

def main():
    with args.csvfile as csvfile:
        output = from_csv(csvfile)

    print(output)

if __name__ == "__main__":
    main()