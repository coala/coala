import sys


if __name__ == "__main__":
    print(input())
    print(sys.argv[1:], file=sys.stderr)
