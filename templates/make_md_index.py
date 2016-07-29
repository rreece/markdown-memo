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
    parser.add_argument('-o', '--out',  default='index.md', type=str,
            help="Some toggle option.")
    return parser.parse_args()


#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
def main():
    ops = options()

    infiles = ops.infiles
    out = ops.out

    rep = r'<h([1-6])\s+[^>]*id="([\w\-]+)"[^>]*>([^<]+)<\/h[1-6]>'

    f_out = open(out, 'w')
    f_out.write('Contents\n')
    f_out.write('---------------------------------------------------\n')
    f_out.write('\n')

    for fn in infiles:
        root, ext = os.path.splitext(fn)

        os.system('pandoc -t html --ascii --smart -o %s-tmp.html %s' % (root, fn))

        f_in = open('%s-tmp.html' % root)
        for line in f_in:
            reo = re.match(rep, line)
            if reo:
                level   = int(reo.group(1))
                id      = reo.group(2)
                name    = reo.group(3)
                if level == 1:
                    f_out.write('%s1.  [%s](%s.html)\n' % ('    '*(level-1), name, root) )
                else:
                    f_out.write('%s1.  [%s](%s.html#%s)\n' % ('    '*(level-1), name, root, id ) )
        f_in.close()

        os.system('rm -f %s-tmp.html' % root)

    f_out.write('\n')
    f_out.close()


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
