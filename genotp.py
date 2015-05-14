#!/usr/bin/env python3
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Last modified: 2015-05-14 22:17:10 +0200
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to genotp.py. This work is published from the
# Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Generates an old-fashioned one-time pad;
65 lines of 12 groups of 5 random capital letters.
"""

from os import urandom


def main():
    ident = '+++++ {} +++++'
    print(ident.format(rndcaps(10)))
    print(otp())


def otp(n=65):
    """Return a one-time pad.

    Arguments:
        n: number of lines in the key

    Returns:
        65 lines of 12 groups of 5 random capital letters.
    """
    lines = []
    for num in range(1, 66):
        i = ['{:02d} '.format(num)]
        i += [rndcaps(5) for j in range(0, 12)]
        lines.append(' '.join(i))
    return '\n'.join(lines)


def rndcaps(n):
    """Generates a string of random capital letters.

    Arguments:
        n: Length of the output string.

    Returns:
        A string of n random capital letters.
    """
    b = urandom(n)
    return ''.join([chr(int(round(c / 10.2)) + 65) for c in b])


if __name__ == '__main__':
    main()
