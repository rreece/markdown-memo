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

    rep_pagetoc = r'\s*<!\-\-\s*PAGETOC\s*\-?\-\->\s*'
    rep_navigation = r'\s*<!\-\-\s*NAVIGATION\s*\-?\-\->\s*'
    rep_preline = r'\s*<div\s*class="">\s*'

    for fn in infiles:
        root, ext = os.path.splitext(fn)
        ext = ext.lstrip('.')
        
        f_in = open(fn)
        fn_out = '%s.tmp.%s' % (root, ext)
        f_out = open(fn_out, 'w')

        for line in f_in:

            reo = None
            newline = line

            ## generate and insert page table of contents
            if not reo:
                reo = re.match(rep_pagetoc, line)
                if reo:
                    pagetoc_md = '%s-pagetoc.md' % root
                    pagetoc_html = '%s-pagetoc.html' % root
                    os.system('python scripts/make_index_md.py -c -1 -4 --out=%s %s' % (pagetoc_md, fn))

                    if os.path.isfile(pagetoc_md):
                        os.system('pandoc -t html --ascii -o %s %s' % (pagetoc_html, pagetoc_md))
                        if os.path.isfile(pagetoc_html):
                            f_pagetoc = open(pagetoc_html)
                            newline = ''.join(f_pagetoc.readlines())
                            f_pagetoc.close()
                            os.system('rm -f %s' % (pagetoc_html))
                        os.system('rm -f %s' % (pagetoc_md))

            ## generate and insert page navigation
            if not reo:
                reo = re.match(rep_navigation, line)
                if reo:
                    newline = make_navigation(fn)

            ## fix preline formatting (literal line breaks for poems)
            if not reo:
                if line.startswith('<div style="white-space: pre-line;">'):
                    newline = '<div class="preline">' + line[36:]
                else:
                    pass
            
            f_out.write(newline)
 
        f_in.close()
        f_out.close()

        assert os.path.isfile(fn_out), fn_out
        os.system('mv -f %s %s' % (fn_out, fn))


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
