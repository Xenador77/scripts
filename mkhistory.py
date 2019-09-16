#!/usr/bin/env python3
# file: mkhistory.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2012-2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2012-04-11T01:41:21+02:00
# Last modified: 2019-09-16T22:03:48+0200
"""Script to format a Git log for LaTeX."""

import os
import re
import subprocess as sp
import sys

# The following texts determine how the commits are generated. Change them to
# suit your preferences.
header = r"""% vim:fileencoding=utf-8:ft=tex
% Automatically generated by mkhistory.py

"""


def main(argv):
    """
    Entry point for mkhistory.

    Arguments:
        argv: command line arguments
    """
    if len(argv) == 1:
        binary = os.path.basename(argv[0])
        print(f"Usage: {binary} outputfilename")
        sys.exit(0)
    fn = argv[1]
    try:
        args = ['git', 'log', '--oneline']
        p = sp.run(args, stdout=sp.PIPE, stderr=sp.DEVNULL, check=True)
        txt = p.stdout.decode()
    except sp.CalledProcessError:
        print("Git not found! Stop.")
        sys.exit(1)
    if fn == '-':
        of = sys.stdout
    else:
        of = open(fn, 'w+')
    of.write(header)
    of.write(fmtlog(txt))
    of.close()


def fmtlog(txt):
    """
    Reformat the text of the one-line log as LaTeX.

    Arguments:
        txt: string to reformat.

    Returns:
        A LaTeX formatted version of the input.
    """
    # Replace TeX special characters in the whole text.
    specials = ('_', '#', '%', r'\$', '{', '}')
    for s in specials:
        txt = re.sub(r'(?<!\\)' + s, '\\' + s, txt)
    # Remove periods at the end of lines.
    txt = re.sub(r'\.$', '', txt, flags=re.MULTILINE)
    lines = txt.split('\n')
    # Remove reference to HEAD
    lines[0] = re.sub(r'\(.*\) ', '', lines[0])
    # Use typewriter font for the commit id.
    lines = [r'\texttt{' + re.sub(' ', r'} ', ln, count=1) for ln in lines if ln]
    return '\\\\\n'.join(lines)


if __name__ == '__main__':
    main(sys.argv)
