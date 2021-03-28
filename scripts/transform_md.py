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

import argparse, sys, time
import os
import re
import glob


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
    rep_pt = r'PlotTable: (.+)$'
    rep_empty = r'\s*$'
    rep_comment = r'//(.+)$'

    for fn in infiles:
        root, ext = os.path.splitext(fn)
        ext = ext.lstrip('.')
        
        f_in = open(fn)
        fn_out = '%s.mdp' % root
        f_out = open(fn_out, 'w')

        cached_lines = None
        pt_part = 0
        ## pt_part 
        ## 0 = not PlotTable
        ## 1 = caption
        ## 2 = empty line
        ## 3 = table data
        ## 4 = empty line

        for line in f_in:

            newline = line

            if pt_part > 0: # parsing PlotTable
                cached_lines.append(newline)

                if pt_part % 2 == 1:
                    if re.match(rep_empty, newline):
                        pt_part += 1
                else:
                    if not re.match(rep_empty, newline):
                        pt_part += 1

                if pt_part >= 4:
                    pt_lines = transform_PlotTable(cached_lines)
                    f_out.writelines(pt_lines)
                    pt_part = 0

                continue

            if not newline[:4] == '    ':  # skip code block

                ## transform [@eq:maxwell] to eq.\ $\eqref{eq:maxwell}$
                reo = re.search(rep_eq, newline)
                if reo:
                    if newline.count('`[@eq:'): # skip inline verbatim `[@eq:
                        pass
                    else:
                        eqlabel = reo.group(1)
                        oldword = reo.group(0)
                        newword = 'eq.\\ $\\eqref{eq:%s}$' % eqlabel
                        newline = newline.replace(oldword, newword)

                if re.match(rep_comment, newline):
                    continue

                ## starting to parse PlotTable
                if re.match(rep_pt, newline):
                    pt_part = 1
                    cached_lines = list()
                    newline = newline.replace('PlotTable', 'Table', 1)
                    cached_lines.append(newline)
                    continue 

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
def transform_PlotTable(lines):

    rep_empty = r'\s*$'
    rep_number = r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
    rep_tbl_label = r'\{#tbl:([a-zA-Z0-9_\-]+)\}'

    part = 1
    caption_lines = list()
    table_lines = list()

    for line in lines:

        if part % 2 == 1:
            if re.match(rep_empty, line):
                part += 1
        else:
            if not re.match(rep_empty, line):
                part += 1

        if part < 3:
            caption_lines.append(line)
        else:
            table_lines.append(line)

    ## find table name
    label = None
    for line in caption_lines:
        reo = re.search(rep_tbl_label, line)
        if reo:
            label = reo.group(1)
            break
    assert label

    ## parse table data
    assert len(table_lines) >= 3
    words = [w.strip() for w in table_lines[0].split('|')]
    columns = words[1:-1]

    table_data = dict()
    for col in columns:
        table_data[col] = list()

    for line in table_lines[2:]:
        words = [w.strip() for w in line.split('|')]
        row_data = words[1:-1]
        for ix, x in enumerate(row_data):
            if re.match(rep_number, x):
                table_data[columns[ix]].append( float(x) )
            else:
                table_data[columns[ix]].append( x )

    out_lines = make_PlotTable(columns, table_data, label)
    out_lines.extend(caption_lines)
    out_lines.extend(table_lines)
    return out_lines


#______________________________________________________________________________
def make_PlotTable(columns, table_data, label):

    import pandas as pd
    import matplotlib
    matplotlib.use("Agg") # suppress the python rocketship icon popup
    import matplotlib.pyplot as plt
    
    # print(plt.style.available) # [u'dark_background', u'bmh', u'grayscale', u'ggplot', u'fivethirtyeight']
    plt.style.use('seaborn-deep')
    plt.rcParams['legend.numpoints'] = 1
    #plt.rcParams['axes.xmargin'] = 0.1
    #plt.rcParams['axes.ymargin'] = 0.1
    #plt.rcParams['figure.figsize'] = (15, 5)

    out_lines = list()

    ## make  plot
    df = pd.DataFrame(table_data)
    ax = df.plot(x=columns[0], y=columns[1:], marker='o', markersize=8)
    fig = ax.get_figure()
    plt.margins(x=0.1, y=0.1, tight=True)
    if fig:
        fig.savefig('img/%s.png' % label, bbox_inches='tight')
        fig.savefig('img/%s.pdf' % label, bbox_inches='tight')
        plt.close()
        cap = 'A plot of [@tbl:%s].' % label
        out_lines.append('![%s](img/%s.png){#fig:%s}\n\n' % (cap, label, label))

    return out_lines


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
