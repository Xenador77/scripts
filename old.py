#!/usr/bin/env python3.4
# vim:fileencoding=utf-8
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2014-02-10 21:43:11 +0100
# Modified: $Date$
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to old.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Renames a directory by prefixing the name with 'old-'. If the directory
name starts with a period, it removes the period and prefixes it with
'old-dot'."""

from __future__ import print_function, division  # 2 and 3 compatibility.

import sys
import os

__version__ = '$Revision$'[11:-2]


def main(argv):
    """Entry point for this script.

    :param argv: command line arguments.
    """
    if len(argv) < 2:
        binary = os.path.basename(argv[0])
        print("{} ver. {}".format(binary, __version__), file=sys.stderr)
        print("Usage: {} directory ...".format(binary), file=sys.stderr)
        sys.exit(1)
    for dirname in argv[1:]:
        if not os.path.isdir(dirname):
            dirwarn = "'{}' is not an existing directory. Skipping."
            print(dirwarn.format(dirname))
            continue
        if dirname.startswith('.'):
            newname = ''.join(['old-dot', dirname[1:]])
        else:
            newname = ''.join(['old-', dirname])
        if os.path.exists(newname):
            renwarn = "'{}' already exists. Skipping rename of '{}'."
            print(renwarn.format(newname, dirname))
            continue
        os.rename(dirname, newname)


if __name__ == '__main__':
    main(sys.argv)