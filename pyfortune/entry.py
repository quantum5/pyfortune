from __future__ import print_function
from pyfortune import list_fortune, fortunepath, Chooser
import sys
import argparse

description = """\
Python reimplementation of the classic fortune.
"""

usage = '%(prog)s [-h] [-aoceflsw] [-n size] [[chance#%%] file]...'

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Python reimplementation of the classic fortune.

When fortune is run with no arguments it prints out a random fortune cookie.
Cookies are divided into several categories.""",
        usage='%(prog)s [-h] [-aoceflsw] [-n size] [[chance#%%] file]...',
        epilog="""
You may specify alternate sayings, by passing a list of sayings as the `file`
argument. These preceded by a percentage, which is a number n between 0 and
100 inclusive, followed by a %. If it is, there will be a n percent chance
that a cookie will be picked from that file. If the percentages do not sum to
100, and there are files without percentages, the remaining probability will
apply to those files, divided into pieces by their relative sizes, unless
`-e` is passed, then all of then gets an equal share.

For example, given two databases 'funny' and 'not-funny', with 'funny' twice
as big (in number of fortunes, not raw file size), saying
    fortune funny not-funny 
will get you fortunes out of funny two-thirds of the time. The command
    fortune 90% funny 10% not-funny 
will pick out 90% of its fortunes from funny (the "10% not-funny" is
unnecessary, since 10% is all that's left).

The -e option says to consider all files equal; thus
    fortune -e funny not-funny
is equivalent to
    fortune 50% funny 50% not-funny
""",
    )
    parser.set_defaults(offend=False)
    parser.set_defaults(long=None)
    parser.add_argument('-a', '--all', action='store_const', dest='offend', const=None,
                        help='Choose from all fortune files, regardless whether the file'
                             ' is marked offensive')
    parser.add_argument('-o', '--offend', action='store_const', dest='offend', const=True,
                        help='Choose from offensive fortune files only')
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
    parser.add_argument('-L', '--language', action='store', dest='lang',
                        help='Display fortunes cookies from a specific language')
    parser.add_argument('-x', '--exclusive', action='store_false', dest='include',
                        help='Exclude the default fortune set, only the set language is shown')
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
    parser.add_argument('fortunes', metavar='FILES', nargs='*',
                        help='fortune files')
    args = parser.parse_args()

    try:
        if args.files:
            for fortune in list_fortune(args.offend):
                print(fortune)
            raise SystemExit

        if args.fortunes:
            percentage = False
            for item in args.fortunes:
                if item.endswith('%'):
                    percentage = True
                    break
            if percentage:
                chances = []
                length = len(args.fortunes)
                index = 0
                while index < length:
                    if args.fortunes[index].endswith('%'):
                        chance = float(args.fortunes[index][:-1]) / 100
                        index += 1
                        try:
                            file = args.fortunes[index]
                        except IndexError:
                            raise SystemExit("%s: Percentage without file!!" % sys.argv[0])
                        chances.append((file, chance))
                    else:
                        chances.append((args.fortunes[index], 0))
                    index += 1
                chooser = Chooser.set_chance(chances, offensive=args.offend, equal=args.equal, lang=args.lang)
            else:
                chooser = Chooser.fromlist(args.fortunes, offensive=args.offend, equal=args.equal, lang=args.lang)
        else:
            chooser = Chooser(offensive=args.offend, equal=args.equal, lang=args.lang, include=args.include)
        file, choice = chooser.choose(long=args.long, size=args.size)
        if choice is None:
            raise SystemExit("%s: Can't find a fortune!!" % sys.argv[0])
        if args.show_file:
            print(file, file=sys.stderr)
        try:
            print(choice)
        except IOError:
            print() # This just happens on windows for no reason, when there are
                    # "special" characters and no new line is printed
        if args.wait:
            try:
                import time
                time.sleep(max(6, len(choice) / 20))
            except KeyboardInterrupt:
                pass
    except ValueError as e:
        print('%s: %s' % (sys.argv[0], e))

if __name__ == '__main__':
    main()
