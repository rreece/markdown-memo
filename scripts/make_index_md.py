#!/usr/bin/env python3
"""
NAME
    make_index.py - make table of contents for markdown-memo

SYNOPSIS
    Put synposis here.

DESCRIPTION
    Put description here.

OPTIONS
    -h, --help
        Prints this manual and exits.
        
    -n VAL
        Blah blah.

AUTHOR
    Ryan Reece  <ryan.reece@cern.ch>

COPYRIGHT
    Copyright 2010 Ryan Reece
    License: GPL <http://www.gnu.org/licenses/gpl.html>
"""

import argparse
from bs4 import BeautifulSoup
import os
import re
import unicodedata


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('infiles',  default=None, nargs='+',
            help='A positional argument.')
    parser.add_argument('-1', '--ignoreone',  default=False,  action='store_true',
            help="Some toggle option.")
    parser.add_argument('-4', '--ignorefour',  default=False,  action='store_true',
            help="Some toggle option.")
    parser.add_argument('-c', '--contents',  default=False,  action='store_true',
            help="Some toggle option.")
    parser.add_argument('-o', '--out',  default='index.md', type=str,
            help="Some toggle option.")
    return parser.parse_args()


def main():
    args = parse_args()

    infiles = args.infiles
    out = args.out

    f_out = open(out, 'w')

    if args.contents:
        f_out.write('### Contents  {.unnumbered}\n')
        f_out.write('\n')

    for fn in infiles:
        root, ext = os.path.splitext(fn)

        os.system('pandoc -t html --ascii --mathjax -o %s.index-tmp.html %s' % (root, fn))

        with open('%s.index-tmp.html' % root) as f_in:
            soup = BeautifulSoup(f_in, 'lxml')
            heading_tags = ["h1", "h2", "h3"]
            heading_tags = list()
            if not args.ignoreone:
                heading_tags.append('h1')
            heading_tags.extend(['h2', 'h3'])
            if not args.ignorefour:
                heading_tags.append('h4')

            for tag in soup.find_all(heading_tags):
                level   = int(tag.name[1:])
                id      = clean_unicode(tag.get('id'))
                name    = tag.text.strip()
                alink   = '%s.html' % root
                if alink == 'index.html':
                    alink = ''

                indent_level = level-1
                if args.ignoreone:
                    indent_level -= 1

                if level == 1:
                    f_out.write('%s1.  **[%s](%s)**\n' % ('    '*indent_level, name, alink) )
                else:
                    f_out.write('%s1.  [%s](%s#%s)\n' % ('    '*indent_level, name, alink, id ) )

        os.system('rm -f %s.index-tmp.html' % root)

    f_out.write('\n')
    f_out.close()


def clean_unicode(s):
    new_s = str(s).strip()

    ## change unicode-hyphen-like characters to ascii
    new_s = new_s.replace(u'\u2010', '-')
    new_s = new_s.replace(u'\u2011', '-')
    new_s = new_s.replace(u'\u2012', '-')
    new_s = new_s.replace(u'\u2013', '-')
    new_s = new_s.replace(u'\u2014', '-')
    new_s = new_s.replace(u'\u2015', '-')

    ## convert unicode to closest ascii for latin-like characters
    ## punctuation-like characters not switched to ascii above will be lost
    ## help from: http://stackoverflow.com/questions/1207457/convert-a-unicode-string-to-a-string-in-python-containing-extra-symbols
    new_s = unicodedata.normalize('NFKD', new_s)
    new_s = new_s.encode('ascii','ignore').decode('utf-8')

    return new_s


if __name__ == '__main__':
    main()
