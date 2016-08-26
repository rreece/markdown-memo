#!/usr/bin/env python
"""
NAME
    name.py - short description

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

SEE ALSO
    ROOT <http://root.cern.ch>

TO DO
    - One.
    - Two.

2011-06-15
"""

#------------------------------------------------------------------------------
# imports
#------------------------------------------------------------------------------

## std
import argparse, sys, time
import os
import re

## my modules

## local modules


#------------------------------------------------------------------------------
# globals
#------------------------------------------------------------------------------
timestamp = time.strftime('%Y-%m-%d-%Hh%M')
GeV = 1000.


#------------------------------------------------------------------------------
# options
#------------------------------------------------------------------------------
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument('infiles',  default=None, nargs='+',
            help='A positional argument.')
#    parser.add_argument('-o', '--out',  default='index.md', type=str,
#            help="Some toggle option.")
    return parser.parse_args()


#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
def main():
    ops = options()

    infiles = ops.infiles
#    out = ops.out

    rep_pagetoc = r'<!\-\-\s*PAGETOC\s*\-?\-\->'

    for fn in infiles:
        root, ext = os.path.splitext(fn)
        
        f_in = open(fn)
        f_out = open('%s-tmp.%s' % (root, ext), 'w')

        for line in f_in:

            reo = None
            newline = line

            if not reo:
                reo = re.match(rep_pagetoc, line)
                if reo:
                    pagetoc_md = '%s-pagetoc.md' % root
                    pagetoc_html = '%s-pagetoc.html' % root
                    os.system('python scripts/make_index_md.py -c -1 -4 --out=%s %s' % (pagetoc_md, fn))

                    if os.path.isfile(pagetoc_md):
                        os.system('pandoc -t html --ascii --standalone --smart -o %s %s' % (pagetoc_html, pagetoc_md))
                        if os.path.isfile(pagetoc_html):
                            f_pagetoc = open(pagetoc_html)
                            newline = ''.join(f_pagetoc.readlines())
                            f_pagetoc.close()
                            os.system('rm -f %s' % (pagetoc_html))
                        os.system('rm -f %s' % (pagetoc_md))

            f_out.write(newline)
 
        f_in.close()
        f_out.close()

        os.system('mv -f %s-tmp.%s %s' % (root, ext, fn))


#------------------------------------------------------------------------------
# free functions
#------------------------------------------------------------------------------

#______________________________________________________________________________
def fatal(message=''):
    sys.exit("Fatal error in %s: %s" % (__file__, message))


#______________________________________________________________________________
def tprint(s, log=None):
    line = '[%s] %s' % (time.strftime('%Y-%m-%d:%H:%M:%S'), s)
    print line
    if log:
        log.write(line + '\n')
        log.flush()


#------------------------------------------------------------------------------
if __name__ == '__main__': main()

# EOF
