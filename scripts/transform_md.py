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
import glob

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
#    parser.add_argument('-o', '--out',  default='default.mdp', type=str,
#            help="Some toggle option.")
    return parser.parse_args()


#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
def main():
    ops = options()

    infiles = ops.infiles
#    out = ops.out

    rep_eq = r'\[@eq:(\w+)\]'

    for fn in infiles:
        root, ext = os.path.splitext(fn)
        ext = ext.lstrip('.')
        
        f_in = open(fn)
        fn_out = '%s.mdp' % root
        f_out = open(fn_out, 'w')

        for line in f_in:

            reo = None
            newline = line

            ## transform [@eq:maxwell] to eq.\ $\eqref{eq:maxwell}$
            if not reo:
                reo = re.search(rep_eq, line)
                if reo:
                    if line[:4] == '    ':  # skip code block
                        pass
                    elif line.count('`[@eq:'): # skip inline `[@eq:
                        pass
                    else:
                        eqlabel = reo.group(1)
                        oldword = reo.group(0)
                        newword = 'eq.\\ $\\eqref{eq:%s}$' % eqlabel
                        newline = newline.replace(oldword, newword)

            f_out.write(newline)
 
        f_in.close()
        f_out.close()

        assert os.path.isfile(fn_out), fn_out


#------------------------------------------------------------------------------
# free functions
#------------------------------------------------------------------------------

#______________________________________________________________________________
def make_navigation(filename):
    mds = list()
    if os.path.isfile('order.txt'):
        f_order = open('order.txt')
        for line in f_order:
            line = line.split('#')[0].strip() # remove comments
            if line:
                mds.append(line)
        f_order.close()
    else:
        mds = glob.glob('*.md')
        if 'index.md' in mds:
            mds.remove('index.md')
        if 'README.md' in mds:
            mds.remove('README.md')
        mds.sort()

    prv = None
    nxt = None
    lst = None

    for fn in mds:
        root, ext = os.path.splitext(fn)
        ext = ext.lstrip('.')

        fn_html = '%s.html' % root
        
        if lst == filename:
            nxt = fn_html
            break
        if fn_html == filename:
            if lst:
                prv = lst
        lst = fn_html

    s = ''

    if prv:
        s += '    <li> <a href="./%s">&#8612;&nbsp;Previous</a> </li>\n' % prv
        
    if nxt:
        s += '    <li> <a href="./%s">&#8614;&nbsp;Next</a> </li>\n' % nxt

    return s

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
