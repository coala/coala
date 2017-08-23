import sys

if __name__ == '__main__':
    data = input()
    try:
        nums = [int(n) for n in data.split()]
    except ValueError:
        print('INVALID INPUT', file=sys.stderr)
    else:
        print(sum(nums))
