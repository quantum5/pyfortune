from __future__ import print_function
from pyfortune import list_fortune, fortunepath, Chooser
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Python reimplementation of the classic cowsay.')
    parser.set_defaults(offend=False)
    parser.set_defaults(long=None)
    parser.add_argument('-a', '--all', action='store_const', dest='offend', const=False,
                        help='Choose from all fortune files, regardless whether the file'
                             ' is marked offensive')
    parser.add_argument('-o', '--offend', action='store_const', dest='offend', const=True,
                        help='Choose from all fortune files, regardless whether the file'
                             ' is marked offensive')
    parser.add_argument('-c', '--show-file', '--cookie-file', action='store_true',
                        dest='show_file', help='Show the cookie file from which the fortune came.')
    parser.add_argument('-e', '--equal', action='store_true', dest='equal',
                        help='Consider all fortune files to be of equal size.')
    parser.add_argument('-f', '--files', action='store_true', dest='files',
                        help='Print out the list of files which would be searched, '
                             "but don't print a fortune.")
    parser.add_argument('-l', '--long', action='store_const', dest='long', const=True,
                        help='Show all fortune cookie that are above the length '
                             'specified in -n')
    parser.add_argument('-s', '--short', action='store_const', dest='long', const=False,
                        help='Show all fortune cookie that are under the length '
                             'specified in -n')
    parser.add_argument('-n', '--size', action='store', dest='size', type=int, default=160,
                        help='Set the longest fortune length (in characters) considered to '
                             'be "short" (the default is 160). All fortunes longer than this '
                             'are considered "long".')
    parser.add_argument('-w', '--wait', action='store_true', dest='wait',
                        help='Wait before termination for an amount of time calculated '
                             'from the number of characters in the message. This is useful if '
                             'it is executed as part of the logout procedure to guarantee that '
                             'the message can be read before the screen is cleared.')
    args = parser.parse_args()

    if args.files:
        for fortune in list_fortune(args.offend):
            print(fortune)
        raise SystemExit
    chooser = Chooser(offensive=args.offend)
    choice = chooser.choose(long=args.long, size=args.size)
    if choice is None:
        raise SystemExit("%s: Can't find a fortune!!" % sys.argv[0])
    print(choice)
    if args.wait:
        import time
        time.sleep(max(6, len(choice) / 20))

if __name__ == '__main__':
    main()
