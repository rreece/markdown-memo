#!/usr/bin/env python3
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

    rep_begin_figure = r'^\\begin{figure}\[\w+\]\s*$'
    rep_begin_table = r'^\\begin{longtable}\[\w\]{([\w\{\}@]+)}\s*$'
    rep_end_table = r'^\\end{longtable}\s*$'
    rep_includegraphics = r'^\\includegraphics{([\w/.\-]+)\.(png|PNG|jpg|jpeg|JPG)}\s*$'

    for fn in infiles:
        root, ext = os.path.splitext(fn)
        ext = ext.lstrip('.')
        
        f_in = open(fn)
        fn_out = '%s.tmp.%s' % (root, ext)
        f_out = open(fn_out, 'w')

        for line in f_in:

            reo = None
            newline = line

            ## force figure float style to be [tp]
            if not reo:
                reo = re.match(rep_begin_figure, line)
                if reo:
                    newline = '\\begin{figure}[tp]\n'
                    
            ## fix begin table?
            if not reo:
                reo = re.match(rep_begin_table, line)
                if reo:
                    # newline = '\\begin{table}[bph]\n'
                    # newline = line.replace('longtable', 'supertabular')
                    pass

            ## fix end table?
            if not reo:
                reo = re.match(rep_end_table, line)
                if reo:
                    # newline = '\\end{table}\n'
                    # newline = line.replace('longtable', 'supertabular')
                    pass

            ## force includegraphics width and height
            if not reo:
                reo = re.match(rep_includegraphics, line)
                if reo:
                    fpath = reo.group(1)
                    suffix = reo.group(2)
                    if os.path.isfile('%s.pdf' % fpath):
                        newline = '\\includegraphics[width=1.0\\linewidth,height=0.75\\linewidth,keepaspectratio]{%s.pdf}\n' % fpath
                    else:
                        newline = '\\includegraphics[width=1.0\\linewidth,height=0.75\\linewidth,keepaspectratio]{%s.%s}\n' % (fpath, suffix)
                        

            f_out.write(newline)
 
        f_in.close()
        f_out.close()

        if os.path.isfile(fn_out):
            os.system('mv -f %s %s' % (fn_out, fn))


#------------------------------------------------------------------------------
# free functions
#------------------------------------------------------------------------------

#______________________________________________________________________________
def fatal(message=''):
    sys.exit("Fatal error in %s: %s" % (__file__, message))


#______________________________________________________________________________
def tprint(s, log=None):
    line = '[%s] %s' % (time.strftime('%Y-%m-%d:%H:%M:%S'), s)
    print(line)
    if log:
        log.write(line + '\n')
        log.flush()


#------------------------------------------------------------------------------
if __name__ == '__main__': main()
