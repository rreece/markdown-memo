#!/usr/bin/env python3
"""
NAME
    make_bib_index_md.py - short description

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

import argparse, sys, time
import os
import re


#------------------------------------------------------------------------------
# options
#------------------------------------------------------------------------------
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',  default='', type=str,
            help='A positional argument.')
    parser.add_argument('-o', '--out',  default='bib_index.md', type=str,
            help="Some toggle option.")
    return parser.parse_args()


#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
def main():
    ops = options()
    infile = ops.infile

    results = parse_file(infile)

    if results:
        write_results(results)


#------------------------------------------------------------------------------
# free functions
#------------------------------------------------------------------------------

#______________________________________________________________________________
def parse_file(infile):
    results = dict()
    f_in = open(infile)
    prev_line = ''
    for line in f_in:
        line = line.split('#')[0].strip() # remove comments
        if line:
            if line.startswith('@'):
                ## e.g. @article{tHooft_2007_The_conceptual_basis_of_quantum_field_theory,
                assert line.count('{')
                citation = line.split('{')[1].rstrip(',').strip()
                ## e.g. tHooft_2007_The_conceptual_basis_of_quantum_field_theory
                ## assume full human-readable citation is on the line above the start of the bibtex entry coming from a markdown2bib.py generation.
                ## e.g. 't Hooft, G. (2007). The conceptual basis of quantum field theory. *Philosophy of Physics, Part A, Handbook of the Philosophy of Science*. http://www.staff.science.uu.nl/~hooft101/lectures/basisqft.pdf
                results[citation] = prev_line
            prev_line = line
    f_in.close()
    return results

#______________________________________________________________________________
def write_results(results):
    ops = options()
    out = ops.out
    f_out = open(out, 'w')
    f_out.write('References to use\n')
    f_out.write('===================================================\n')
    f_out.write('\n')
    footnotes = dict()
    citations = results.keys()
    citations.sort()
#    for citation, ref in results.iteritems():
    for citation in citations:
        ref = results[citation]
        shortauthor = citation.split('_')[0] + citation.split('_')[1] # author + year
        sa = shortauthor
        if footnotes.has_key(shortauthor):
            ch = shortauthor[-1]
            if ord(ch) >= 97:
                sa = shortauthor[:-1] + chr(ord(ch)+1)
            else:
                ch = 'a'
                old_citation = footnotes.pop(shortauthor, None)
                old_shortauthor = shortauthor + ch
                footnotes[old_shortauthor] = old_citation
                sa = shortauthor + chr(ord(ch)+1)
        footnotes[sa] = citation

    footkeys = footnotes.keys()
    footkeys.sort()

    for shortauthor in footkeys:
        citation = footnotes[shortauthor]
        f_out.write('1.  `%s`[^%s]\n' % (citation, shortauthor))

    f_out.write('\n')

    for shortauthor in footkeys:
        citation = footnotes[shortauthor]
        f_out.write('[^%s]: @%s\\.\n' % (shortauthor, citation))

    f_out.write('\n')
    f_out.write('<!-- REFERENCES -->\n')
    f_out.write('\n')
    f_out.close()

    print('')
    print('%s written. %s items.' % (out, len(footnotes)))
    print('')


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
