import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-o", help="override output name", metavar="NAME")
parser.add_argument("file", help="input protobuf file")

def main():
    args = parser.parse_args()
    if args.verbose:
        print "verbosity turned on"

if __name__ == '__main__':
    main()
