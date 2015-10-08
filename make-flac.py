#!/usr/bin/env python3
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2014-08-12 14:37:50 +0200
# Last modified: 2015-10-08 21:58:49 +0200
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to make-flac.py. This work is published from
# the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Encodes WAV files from cdparanoia to FLAC format. Processing is
done in parallel using as many subprocesses as the machine has
cores. Title and song information is gathered from a text file called
titles.
"""

__version__ = '1.1.0'

from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
import argparse
import os
import logging
import subprocess
import sys

Trackinfo = namedtuple('Trackinfo', ['num', 'title', 'artist', 'album',
                                     'ifname', 'ofname'])


def main(argv):
    """
    Entry point for make-flac.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', default='warning',
                        choices=['debug', 'info', 'warning', 'error'],
                        help="logging level (defaults to 'warning')")
    parser.add_argument('-v', '--version',
                        action='version',
                        version=__version__)
    args = parser.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log.upper(), None),
                        format='%(levelname)s: %(message)s')
    logging.debug('command line arguments = {}'.format(argv))
    logging.debug('parsed arguments = {}'.format(args))

    checkfor('flac')
    procs = []
    tracks = trackdata()
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as tp:
        convs = tp.map(runflac, tracks)
    convs = [(tr, rv) for tr, rv in convs if rv != 0]
    for fn, rv in convs:
        print('Conversion of {} failed, return code {}'.format(fn, rv))


def checkfor(args, rv=0):
    """
    Make sure that a program necessary for using this script is available.

    Arguments:
        args: String or list of strings of commands. A single string may
            not contain spaces.
        rv: Expected return value from evoking the command.
    """
    if isinstance(args, str):
        if ' ' in args:
            raise ValueError('no spaces in single command allowed')
        args = [args]
    try:
        rc = subprocess.call(args, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        if rc != rv:
            raise OSError
        logging.info('found required program "{}".'.format(args[0]))
    except OSError as oops:
        outs = "required program '{}' not found: {}."
        logging.error(outs.format(args[0], oops.strerror))
        sys.exit(1)


def trackdata(fname='titels'):
    """
    Read the data describing the tracks from a text file.

    Arguments:
        fname: name of the text file describing the tracks.

    This file has the following format:

      album title
      artist
      01 title of 1st song
      ..
      14 title of 14th song

    Returns:
        A list of Trackinfo objects.
    """
    tracks = []
    try:
        with open(fname, 'r') as tf:
            lines = tf.readlines()
    except IOError:
        logging.error('i/o error reading "{}", no tracks found.'.format(fname))
        sys.exit(1)
    album = lines.pop(0).strip()
    artist = lines.pop(0).strip()
    for l in lines:
        words = l.split()
        if not words:
            continue
        num = int(words.pop(0))
        # These are the default WAV file names generated by cdparanoia.
        ifname = 'track{:02d}.cdda.wav'.format(num)
        if os.access(ifname, os.R_OK):
            ofname = 'track{:02d}.flac'.format(num)
            title = ' '.join(words)
            tracks.append(Trackinfo(num, title, artist, album, ifname,
                                    ofname))
    if not tracks:
        logging.error('no tracks found.')
        sys.exit(1)
    return tracks


def runflac(tinfo):
    """Use the flac(1) program to convert a music file to FLAC format.

    Arguments:
        tinfo: A Trackinfo object

    Returns:
        A tuple containing the Trackinfo and the return value of flac.
    """
    args = ['flac', '--best', '--totally-silent', '-TARTIST=' + tinfo.artist,
            '-TALBUM=' + tinfo.album, '-TTITLE=' + tinfo.title,
            '-TTRACKNUM={:02d}'.format(num), '-o', tinfo.ofname, tinfo.ifname]
    logging.info('started conversion of "{}" to "{}"'.format(tinfo.title,
                                                             tinfo.ofname))
    rv = subprocess.call(args, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    logging.info('finished "{}"'.format(tinfo.ofname))
    return (tinfo, rv)


if __name__ == '__main__':
    main(sys.argv[1:])
