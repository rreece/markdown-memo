#!/usr/bin/env python
"""
NAME
    markdown2bib.py - Converts simple markdown-formatted APA bibliographies to bibtex

SYNOPSIS
    markdown2bib.py [-h] [-o OUTPUT] infiles [infiles ...]

DESCRIPTION
    Scrape the world's bibliographies!
    All your bibs are belong to us.

OPTIONS
    -h, --help
        Prints this manual and exits.
        
    -o OUTFILE
        Specifies the output filename (out.bib by default).

AUTHOR
    Ryan Reece  <ryan.reece@cern.ch>

COPYRIGHT
    Copyleft 2016 Ryan Reece
    License: GPL <http://www.gnu.org/licenses/gpl.html>

2016-03-15
"""

#------------------------------------------------------------------------------
# imports
#------------------------------------------------------------------------------

## std
import argparse, sys, time
import re
import textwrap
import unicodedata

## my modules

## local modules


#------------------------------------------------------------------------------
# globals
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# options
#------------------------------------------------------------------------------
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument('infiles',  default=None, nargs='+',
            help='Input text files of APA references.')
#    parser.add_argument('-x', '--option',  default=False,  action='store_true',
#            help="Some toggle option.")
#    parser.add_argument('-i', '--input',  default=None,
#            help="Path to directory of datasets")
    parser.add_argument('-o', '--output',  default='out.bib',
            help="Name of output file.")   
    return parser.parse_args()


#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
def main():
    ops = options()

    results = dict()

    for infile in ops.infiles:
        print '|  Parsing file: %s' % infile
        new_results = parse_file(infile) 
        results.update(new_results)

    if results:
        keys = results.keys()
        keys.sort()
        articles = []
        books = []
        incollections = []
        miscs = []
        errors = []

        ## count the articles, books, ...
        for k in keys:
            ctype, citation, bibtex = results[k]
            if ctype == 'article':
                articles.append(citation)
            elif ctype == 'book':
                books.append(citation)
            elif ctype == 'incollection':
                incollections.append(citation)
            elif ctype == 'misc':
                miscs.append(citation)
            else:
                errors.append(k)

        print '|'
        print '|  %i entries found.' % len(results)
        print '|  - %3i articles' % len(articles)
        print '|  - %3i incollections' % len(incollections)
        print '|  - %3i books' % len(books)
        print '|  - %3i miscs' % len(miscs)
        print '|  - %3i errors' % len(errors)
        print '|'

        ## write header
        timestamp = time.strftime('%Y-%m-%d-%Hh%M')
        f_out = open(ops.output, 'w')
        f_out.write('## bibtex references file\n')
        f_out.write('## gerenated by markdown_bib.py\n')
        f_out.write('## created: %s\n' % timestamp)
        f_out.write('###############################################################################\n\n')

        ## write lists of the markdown citations to use
        f_out.write('Total Entries: %i\n\n' % len(results))
        
        f_out.write('Articles: %i\n' % len(articles))
        for a in articles:
            f_out.write('%s\n' % a)
        f_out.write('\n')

        f_out.write('Incollections: %i\n' % len(incollections))
        for a in incollections:
            f_out.write('%s\n' % a)
        f_out.write('\n')

        f_out.write('Books: %i\n' % len(books))
        for a in books:
            f_out.write('%s\n' % a)
        f_out.write('\n')

        f_out.write('Miscs: %i\n' % len(miscs))
        for a in miscs:
            f_out.write('%s\n' % a)
        f_out.write('\n')

        if errors:
            f_out.write('ERRORS: %i\n' % len(books))
            for a in errors:
                f_out.write('%s\n' % a)
            f_out.write('\n')

        f_out.write('###############################################################################\n\n')

        ## write the bibtex entries
        for k in keys:
            ctype, citation, bibtex = results[k]
            f_out.write(k)
            f_out.write('\n')
            if ctype:
                f_out.write(bibtex)
                f_out.write('\n\n')
            else:
                f_out.write('PARSING ERROR\n\n')

        f_out.close()
        print '|  %s written.' % ops.output

    print '|'
    print '|  Done!  _______,,,^..^,,,_~_______'
    print '|'


#------------------------------------------------------------------------------
# free functions
#------------------------------------------------------------------------------

#______________________________________________________________________________
def parse_file(infile):
    results = dict()
    f_in = open(infile)
    for line in f_in:
        line = line.split('#')[0].strip() # remove comments
        if line:
            results[line] = parse_line(line) # type, citation, bibtex
    f_in.close()
    return results


#______________________________________________________________________________
def parse_line(line):
    """
    Using the APA citation style.
    https://www.zotero.org/styles
    """
    # Weinberg, S. (1995). *Quantum Theory of Fields, Vol. 1*. Cambridge University Press.
    rep_book = ''.join([r"(?P<author>[^()]+)",
                        r"\s+\((?P<year>\d+)\)[,.]",
                        r"\s+\*(?P<title>[^*]+)\*[,.]?",
                        r"(\s+\((?P<edition>\d+)\S+\s+ed\.\)[,.]?)?",
                        r"((?!\s+https?://)\s+((?P<address>[^.:\[\]]+):\s+)?(?P<publisher>[^.\[\]]+))?[,.]?",
                        r"(\s+(Retrieved\s+from\s+)?(?P<url>https?://\S+)[,.]?)?",
                        r"(\s+\[?(?P<note>[^\[\]]+)\]?\.?)?",
                        ])
    # Redhead, M. (1988). A Philosopher Looks at Quantum Field Theory. In H. Brown & R. Harr\'{e} (Eds.), Philosophical Foundations of Quantum Field Theory (pp. 9-23). Oxford: Clarendon Press.
    rep_incollection = ''.join([r"(?P<author>[^()]+)",
                        r"\s+\((?P<year>\d+)\)[,.]",
                        r"\s+(?P<title>[^.?!\[\]]+[?!]?)[,.]?",
                        r"\s+In",
                        r"(\s+(?P<editor>[^()]+)\s+\(Eds?\.\)[,.]?)?",
                        r"(?!\s+https?://)(\s+\*(?P<booktitle>[^()]+)\*[,.]?)",
                        r"(\s+\(((?P<edition>\d+)\S+\s+ed\.,?\s*)?p+\.\s+(?P<pages>\d+-*\d*)\)[,.]?)?",
                        r"(?!\s+https?://)(\s+((?P<address>[^.:\[\]]+):\s+)?(?P<publisher>[^.\[\]]+))?[,.]?",
                        r"(\s+(Retrieved\s+from\s+)?(?P<url>https?://\S+)[,.]?)?",
                        r"(\s+\[?(?P<note>[^\[\]]+)\]?\.?)?",
                        ])
    # Baker, D. J. (2009). Against field interpretations of quantum field theory. *The British Journal for the Philosophy of Science*, 60(3), 585--609.
    # Baker, D.J. (2015). The Philosophy of Quantum Field Theory. [Preprint]
    rep_article = ''.join([r"(?P<author>[^()]+)",
                        r"\s+\((?P<year>\d+)\)[,.]",
                        r"\s+(?P<title>[^.?!\[\]]+[?!]?)[,.]?",
                        r"(?!\s+https?://)(\s+\*(?P<journal>[^*]+)\*[,.]?)",
                        r"(\s+\*?(?P<volume>\d+)\*?(\((?P<number>\d+)\))?[,.]?)?",
                        r"(\s+(?P<pages>\d+-*\d*)[,.]?)?",
                        r"(\s+(Retrieved\s+from\s+)?(?P<url>https?://\S+)[,.]?)?",
                        r"(\s+\[?(?P<note>[^\[\]]+)\]?\.?)?",
                        ])
    # ATLAS Collaboration. (2011). Updated Luminosity Determination in pp Collisions at $\sqrt{s}=7 TeV using the ATLAS Detector. ATLAS-CONF-2010-011. http://cdsweb.cern.ch/record/1334563
    rep_misc = ''.join([r"(?P<author>[^()]+)",
                        r"\s+\((?P<year>\d+)\)[,.]",
                        r"\s+(?P<title>[^.?!\[\]]+[?!]?)[,.]?",
                        r"((?!\s+https?://)\s+(?P<howpublished>[^.\[\]]+)[,.]?)?",
                        r"(\s+(Retrieved\s+from\s+)?(?P<url>https?://\S+)[,.]?)?",
                        r"(\s+\[?(?P<note>[^\[\]]+)\]?\.?)?",
                        ])

    reo = re.match(rep_book, line)
    if reo:
        ## parse book
        print '|  Book: %s' % trim_string(line)
        citation, bibtex = make_book(reo)
        return 'book', citation, bibtex

    else:
        reo = re.match(rep_incollection, line)
        if reo:
            ## parse incollection
            print '|  Incollection: %s' % trim_string(line)
            citation, bibtex = make_incollection(reo)
            return 'incollection', citation, bibtex

        else:
            reo = re.match(rep_article, line)
            if reo:
                ## parse article
                print '|  Article: %s' % trim_string(line)
                citation, bibtex = make_article(reo)
                return 'article', citation, bibtex

            else:
                reo = re.match(rep_misc, line)
                if reo:
                    ## parse misc
                    print '|  Misc: %s' % trim_string(line)
                    citation, bibtex = make_misc(reo)
                    return 'misc', citation, bibtex

                else:
                    print '|  NO MATCH: %s' % trim_string(line)

    return None, None, None


#______________________________________________________________________________
def make_book(reo):
    """
    @book{Author_year_title,
        author      = {},
        year        = {2000},
        title       = {},
        edition     = {2},  # optional
        address     = {},   # optional
        publisher   = {},   # optional
        url         = {},   # optional
    }
    """
#    mds = []
#    mds.append("%s (%s). *%s*." % (reo.group('author'), reo.group('year'), reo.group('title')))
#    if reo.group('address') and reo.group('publisher'):
#        mds.append(" %s: %s." % (reo.group('address'), reo.group('publisher')))
#    elif reo.group('publisher'):
#        mds.append(" %s." % reo.group('publisher'))
#    if reo.group('url'):
#        mds.append(" %s." % reo.group('url'))
#    if reo.group('note'):
#        mds.append(" [%s]." % reo.group('note'))
#    md = ''.join(mds)

    lines = []
    cite_author = reo.group('author').split()[0].rstrip(',')
    cite_year = reo.group('year')
    cite_title = reo.group('title')
    max_title_len = 50
    if len(cite_title) > max_title_len:
        cite_title = textwrap.fill(cite_title, max_title_len).split('\n')[0]
#    cite_title = clean_citation(cite_title)
    citation = '%s_%s_%s' % (cite_author, cite_year, cite_title)
    citation = clean_citation(citation)
    lines.append('@book{%s,' % citation)
    author = reo.group('author')
    author = author.replace('&', 'and')
    lines.append('    author      = {%s},' % author)
    lines.append('    year        = {%s},' % reo.group('year'))
    lines.append('    title       = "{%s}",' % reo.group('title'))
    if reo.group('edition'):
        lines.append('    edition     = {%s},' % reo.group('edition'))
    if reo.group('address'):
        lines.append('    address     = {%s},' % reo.group('address'))
    if reo.group('publisher'):
        lines.append('    publisher   = {%s},' % reo.group('publisher'))
    if reo.group('url'):
        lines.append('    url         = {%s},' % reo.group('url'))
    if reo.group('note'):
        lines.append('    note        = {%s},' % reo.group('note'))
    lines.append('}')
    s = '\n'.join(lines)
    return citation, s


#______________________________________________________________________________
def make_incollection(reo):
    """
    @incollection{Redhead_1988_philosopher_looks_at_QFT,
        author      = {Redhead, M.L.G.},
        year        = {1988},
        title       = "{A Philosopher Looks at Quantum Field Theory}",
        editor      = {Brown, H. and R. Harr\'{e}},
        booktitle   = "{Philosophical Foundations of Quantum Field Theory}",
        edition     = {2},
        publisher   = {Clarendon Press},
        address     = {Oxford},
        pages       = {9--23},
        chapter     = {1},
    }
    """
    lines = []
    cite_author = reo.group('author').split()[0].rstrip(',')
    cite_year = reo.group('year')
    cite_title = reo.group('title')
    max_title_len = 50
    if len(cite_title) > max_title_len:
        cite_title = textwrap.fill(cite_title, max_title_len).split('\n')[0]
#    cite_title = clean_citation(cite_title)
    citation = '%s_%s_%s' % (cite_author, cite_year, cite_title)
    citation = clean_citation(citation)
    lines.append('@incollection{%s,' % citation)
    author = reo.group('author')
    author = author.replace('&', 'and')
    lines.append('    author      = {%s},' % author)
    lines.append('    year        = {%s},' % reo.group('year'))
    lines.append('    title       = "{%s}",' % reo.group('title'))
    if reo.group('edition'):
        lines.append('    edition     = {%s},' % reo.group('edition'))
    if reo.group('editor'):
        editor = reo.group('editor')
        editor = editor.replace('&', 'and')
        lines.append('    editor      = {%s},' % editor)
    lines.append('    booktitle   = "{%s}",' % reo.group('booktitle'))
    if reo.group('pages'):
        pages = reo.group('pages')
        pages = pages.replace('---', '-')
        pages = pages.replace('--', '-')
        pages = pages.replace('-', '--') ## force double -- e.g. 3--20
        lines.append('    pages       = {%s},' % pages)
    if reo.group('address'):
        lines.append('    address     = {%s},' % reo.group('address'))
    if reo.group('publisher'):
        lines.append('    publisher   = {%s},' % reo.group('publisher'))
    if reo.group('url'):
        lines.append('    url         = {%s},' % reo.group('url'))
    if reo.group('note'):
        lines.append('    note        = {%s},' % reo.group('note'))
    lines.append('}')
    s = '\n'.join(lines)
    return citation, s


#______________________________________________________________________________
def make_article(reo):
    """
    @article{Author_year_title,
        author      = {},
        year        = {},
        title       = "{}",
        journal     = {},
        volume      = "{1}",  # optional
        number      = {1},  # optional
        pages       = {},   # optional
        url         = {},   # optional
    }
    """
    lines = []
    cite_author = reo.group('author').split()[0].rstrip(',')
    cite_year = reo.group('year')
    cite_title = reo.group('title')
    max_title_len = 50
    if len(cite_title) > max_title_len:
        cite_title = textwrap.fill(cite_title, max_title_len).split('\n')[0]
#    cite_title = clean_citation(cite_title)
    citation = '%s_%s_%s' % (cite_author, cite_year, cite_title)
    citation = clean_citation(citation)
    lines.append('@article{%s,' % citation)
    author = reo.group('author')
    author = author.replace('&', 'and')
    lines.append('    author      = {%s},' % author)
    lines.append('    year        = {%s},' % reo.group('year'))
    lines.append('    title       = "{%s}",' % reo.group('title'))
    if reo.group('journal'):
        lines.append('    journal     = {%s},' % reo.group('journal'))
    if reo.group('volume'):
        lines.append('    volume      = "{%s}",' % reo.group('volume'))
    if reo.group('number'):
        lines.append('    number      = {%s},' % reo.group('number'))
    if reo.group('pages'):
        pages = reo.group('pages')
        pages = pages.replace('---', '-')
        pages = pages.replace('--', '-')
        pages = pages.replace('-', '--') ## force double -- e.g. 3--20
        lines.append('    pages       = {%s},' % pages)
    if reo.group('url'):
        lines.append('    url         = {%s},' % reo.group('url'))
    if reo.group('note'):
        lines.append('    note        = {%s},' % reo.group('note'))
    lines.append('}')
    s = '\n'.join(lines)
    return citation, s


#______________________________________________________________________________
def make_misc(reo):
    """
    @misc{Author_year_title,
        author      = {},
        year        = {},
        title       = "{}",
        howpublished = "{}",
        note        = {},   # optional
        url         = {},   # optional
    }
    """
    lines = []
    cite_author = reo.group('author').split()[0].rstrip(',')
    cite_year = reo.group('year')
    cite_title = reo.group('title')
    max_title_len = 50
    if len(cite_title) > max_title_len:
        cite_title = textwrap.fill(cite_title, max_title_len).split('\n')[0]
#    cite_title = clean_citation(cite_title)
    citation = '%s_%s_%s' % (cite_author, cite_year, cite_title)
    citation = clean_citation(citation)
    lines.append('@misc{%s,' % citation)
    author = reo.group('author')
    author = author.replace('&', 'and')
    lines.append('    author      = {%s},' % author)
    lines.append('    year        = {%s},' % reo.group('year'))
    lines.append('    title       = "{%s}",' % reo.group('title'))
    if reo.group('howpublished'):
        lines.append('    howpublished = "{%s}",' % reo.group('howpublished'))
    if reo.group('url'):
        lines.append('    url         = {%s},' % reo.group('url'))
    if reo.group('note'):
        lines.append('    note        = {%s},' % reo.group('note'))
    lines.append('}')
    s = '\n'.join(lines)
    return citation, s


#______________________________________________________________________________
def clean_citation(fn):
    new_fn = str(fn)

    ## remove extra spaces and convert to '-'
    new_fn = new_fn.strip()
    u_new_fn = unicode(new_fn, 'utf-8')

    ## change unicode-hyphen-like characters to ascii
    u_new_fn = u_new_fn.replace(u'\u2010', '-')
    u_new_fn = u_new_fn.replace(u'\u2011', '-')
    u_new_fn = u_new_fn.replace(u'\u2012', '-')
    u_new_fn = u_new_fn.replace(u'\u2013', '-')
    u_new_fn = u_new_fn.replace(u'\u2014', '-')
    u_new_fn = u_new_fn.replace(u'\u2015', '-')

    ## convert unicode to closest ascii for latin-like characters
    ## punctuation-like characters not switched to ascii above will be lost
    ## help from: http://stackoverflow.com/questions/1207457/convert-a-unicode-string-to-a-string-in-python-containing-extra-symbols
    u_new_fn = unicodedata.normalize('NFKD', u_new_fn)
    u_new_fn = u_new_fn.encode('ascii','ignore')
    new_fn = str(u_new_fn)

    ## remove redundant space (' ' and '_' converted to '-')
    new_fn = new_fn.replace('     ', ' ')
    new_fn = new_fn.replace('    ', ' ')
    new_fn = new_fn.replace('   ', ' ')
    new_fn = new_fn.replace('  ', ' ')
    new_fn = new_fn.replace(' ', '-')
    new_fn = new_fn.replace('_____', ' ')
    new_fn = new_fn.replace('____', ' ')
    new_fn = new_fn.replace('___', ' ')
    new_fn = new_fn.replace('__', ' ')
    new_fn = new_fn.replace('_', '-')
    new_fn = new_fn.replace('-----', '-')
    new_fn = new_fn.replace('----', '-')
    new_fn = new_fn.replace('---', '-')
    new_fn = new_fn.replace('--', '-')
    new_fn = new_fn.replace('.-', '.')
    new_fn = new_fn.replace('-.', '.')

    ## remove strange characters
    len_fn = len(new_fn)
    i = 0
    while i < len_fn:
        ch = new_fn[i]
        if not re.match(r'[a-zA-Z0-9_.\-]', ch): # \w = [a-zA-Z0-9_]
            new_fn = new_fn.replace(ch, '_')
            len_fn = len(new_fn)
        i += 1
    new_fn = new_fn.replace('_', '')

    ## remove '.'
    new_fn = new_fn.replace('.', '')

    ## convert all '-' to '_'
    new_fn = new_fn.replace('-', '_')

    ## chop-off article words
    new_fn_lower = new_fn.lower()
    if new_fn_lower.endswith('_and'):
        new_fn = new_fn[:-4]
    if new_fn_lower.endswith('_a'):
        new_fn = new_fn[:-2]
    if new_fn_lower.endswith('_an'):
        new_fn = new_fn[:-3]
    if new_fn_lower.endswith('_the'):
        new_fn = new_fn[:-4]

    return new_fn


#______________________________________________________________________________
def check_for_url(s=''):
    rep = r"(https?://\S+)"
    reo = re.search(rep, s)
    if reo:
        url = reo.group(1)
        before, after = s.split(url, 1)
        return url, before, after
    return None


#______________________________________________________________________________
def trim_string(s, maxl=70):
    if len(s) > maxl:
        s = s[:maxl-3] + '...'
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

#------------------------------------------------------------------------------
# examples
# 
# @article{Author_year_title,
#     author      = {},
#     year        = {},
#     title       = {},
#     journal     = {},
#     volume      = {1},  # optional
#     pages       = {},   # optional
#     url         = {},   # optional
# }
# 
# @book{Author_year_title,
#     author      = {},
#     year        = {2000},
#     title       = {},
#     edition     = {2},  # optional
#     address     = {},   # optional
#     publisher   = {},   # optional
#     url         = {},   # optional
# }
# 
# @incollection{Redhead_1988_philosopher_looks_at_QFT,
#     author      = {Redhead, Michael},
#     year        = {1988},
#     title       = {A Philosopher Looks at Quantum Field Theory},
#     editor      = {Brown, H. and R. Harr\'{e}},
#     booktitle   = {Philosophical Foundations of Quantum Field Theory},
#     edition     = {2},  # optional
#     publisher   = {Clarendon Press},
#     address     = {Oxford},
#     pages       = {9--23},
#     chapter     = {1},
# }
#
#------------------------------------------------------------------------------

# EOF
