#!/usr/bin/env python3

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
        
e   -o OUTFILE
        Specifies the output filename (out.bib by default).

AUTHOR
    Ryan Reece  <ryan.reece@gmail.com>

COPYRIGHT
    Copyleft 2016 Ryan Reece
    License: GPL <http://www.gnu.org/licenses/gpl.html>

2016-03-15
"""

import argparse
import os
import re
import sys
import textwrap
import time
import unicodedata


#------------------------------------------------------------------------------
# globals
#------------------------------------------------------------------------------

# Note: \w = [a-zA-Z0-9_], \S = [^ \t\n\r\f\v]

# Baker, D.J. (2009). Against field interpretations of quantum field theory. *The British Journal for the Philosophy of Science*, 60(3), 585--609.
# Baker, D.J. (2015). The Philosophy of Quantum Field Theory. [Preprint]
rep_article_s = ''.join([r"(?P<author>((\{[^}]+\})|([^(),.]+(,\s+\w\.(\s*\w\.)?(\s*\w\.)?)?(,?\s+(&\s+)?)?){1,6}(\s+et\s+al\.)?))[,.]?",
#rep_article_s = ''.join([r"(?P<author>\{[^}]+\})[,.]?",
                    r"\s+\((?P<year>\d+)\)[,.]",
#                    r"\s+(?P<title>[^.?!\[\]]+[?!]?)[,.]?",
                    r"\s+(?P<title>[^*\[\]]+)[,.]?",
                    r"(?!\s+<?https?://)(\s+\*(?P<journal>[^*]+)\*[,.]?)",
                    r"(\s+\*?(?P<volume>\d+)\*?(\((?P<number>\d+)\))?[,.]?)?",
                    r"(\s+(?P<pages>(P|p)?\w?\d+-*\w?\d*)[,.]?)?",
                    r"(\s+(Retrieved\s+from\s+)?<?(?P<url>https?://[^ \t\n\r\f\v<>]+)>?[,.]?)?",
                    r"(\s+\[?(?P<note>[^\[\]]+)\]?\.?)?",
                    ])
rep_article = re.compile(rep_article_s)
# Weinberg, S. (1995). *Quantum Theory of Fields, Vol. 1*. Cambridge University Press.
rep_book_s = ''.join([r"(?P<author>([^(),.]+(,\s+\w\.(\s*\w\.)?(\s*\w\.)?)?(,?\s+(&\s+)?)?){1,6}(\s+et\s+al\.)?)[,.]?",
                    r"\s+\((?P<year>\d+)\)[,.]",
                    r"\s+\*(?P<title>[^*]+)\*[,.]?",
                    r"(\s+\((?P<edition>\d+)\w*\s+ed\.\)[,.]?)?",
                    r"(\s+\(((?P<editor>[^()]+),\s+[Ee]ds?\.)?(\s+&\s+)?((?P<translator>[^()]+),\s+[Tt]rans\.)?\)[,.]?)?",
                    r"((?!\s+<?https?://)\s+((?P<address>[^.:\[\]]+):\s+)?(?P<publisher>[^.\[\]]+))?[,.]?",
                    r"(\s+(Retrieved\s+from\s+)?<?(?P<url>https?://[^ \t\n\r\f\v<>]+)>?[,.]?)?",
                    r"(\s+\[?(?P<note>[^\[\]]+)\]?\.?)?",
                    ])
rep_book = re.compile(rep_book_s)
# Redhead, M. (1988). A Philosopher Looks at Quantum Field Theory. In H. Brown & R. Harr\'{e} (Eds.), Philosophical Foundations of Quantum Field Theory (pp. 9-23). Oxford: Clarendon Press.
rep_incollection_s = ''.join([r"(?P<author>([^(),.]+(,\s+\w\.(\s*\w\.)?(\s*\w\.)?)?(,?\s+(&\s+)?)?){1,6}(\s+et\s+al\.)?)[,.]?",
                    r"\s+\((?P<year>\d+)\)[,.]",
                    r"\s+(?P<title>[^.?!\[\]]+[?!]?)[,.]?",
                    r"\s+In",
                    r"(\s+(?P<editor>[^()*]+)(\s+\([Ee]ds?\.\))?[,.]?)?",
                    r"(?!\s+<?https?://)(\s+\*(?P<booktitle>[^*]+)\*[,.]?)",
                    r"(\s+\(((?P<edition>\d+)\w*\s+ed\.,?\s*)?p+\.\s+(?P<pages>(P|p)?\d+-*\d*)\)[,.]?)?",
                    r"(?!\s+<?https?://)(\s+((?P<address>[^.:\[\]]+):\s+)?(?P<publisher>[^.\[\]]+))?[,.]?",
                    r"(\s+(Retrieved\s+from\s+)?<?(?P<url>https?://[^ \t\n\r\f\v<>]+)>?[,.]?)?",
                    r"(\s+\[?(?P<note>[^\[\]]+)\]?\.?)?",
                    ])
rep_incollection = re.compile(rep_incollection_s)
# ATLAS Collaboration. (2011). Updated Luminosity Determination in pp Collisions at $\sqrt{s}=7 TeV using the ATLAS Detector. ATLAS-CONF-2010-011. http://cdsweb.cern.ch/record/1334563
rep_misc_s = ''.join([r"(?P<author>([^(),.]+(,\s+\w\.(\s*\w\.)?(\s*\w\.)?)?(,?\s+(&\s+)?)?){1,6}(\s+et\s+al\.)?)[,.]?",
                    r"\s+\((?P<year>\d+)\)[,.]",
                    r"\s+(?P<title>[^.?!\[\]]+[?!]?)[,.]?",
                    r"((?!\s+<?https?://)\s+(?P<howpublished>[^.\[\]]+)[,.]?)?",
                    r"(\s+(Retrieved\s+from\s+)?<?(?P<url>https?://[^ \t\n\r\f\v<>]+)>?[,.]?)?",
                    r"(\s+\[?(?P<note>[^\[\]]+)\]?\.?)?",
                    ])
rep_misc = re.compile(rep_misc_s)
rep_author_s = r"(?P<a1>[^(),.]+(,\s+\w\.(\s*\w\.)?(\s*\w\.)?)?)(?P<etal>\s+et\s+al)?(,?\s+(&\s+)?(?P<a2>[^(),.]+(,\s+\w\.(\s*\w\.)?(\s*\w\.)?)?))?(,?\s+(&\s+)?(?P<a3>[^(),.]+(,\s+\w\.(\s*\w\.)?(\s*\w\.)?)?))?(,?\s+(&\s+)?(?P<a4>[^(),.]+(,\s+\w\.(\s*\w\.)?(\s*\w\.)?)?))?(,?\s+(&\s+)?(?P<a5>[^(),.]+(,\s+\w\.(\s*\w\.)?(\s*\w\.)?)?))?(,?\s+(&\s+)?(?P<a6>[^(),.]+(,\s+\w\.(\s*\w\.)?(\s*\w\.)?)?))?"
rep_author = re.compile(rep_author_s)
rep_url_s = r"<?(https?://[^ \t\n\r\f\v<>]+)>?"
rep_url = re.compile(rep_url_s)
rep_ascii_s = r'[a-zA-Z0-9_.\-]'
rep_ascii = re.compile(rep_ascii_s)


#------------------------------------------------------------------------------
# options
#------------------------------------------------------------------------------
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument('infiles',  default=None, nargs='+',
            help='Input text files of APA references.')
    parser.add_argument('-v', '--verbose',  default=False,  action='store_true',
            help="Some toggle option.")
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
        print('Parsing file: %s' % infile)
        new_results = parse_file(infile) 
        results.update(new_results)

    if results:
        keys = list(results.keys())
        keys.sort()
        articles = []
        books = []
        incollections = []
        miscs = []
        errors = []
        duplicates = []
        allcitations = []
        lowallcitations = []

        ## count the articles, books, ...
        for k in keys:
            ctype, citation, bibtex = results[k]
            low_citation = citation.lower()
            if not low_citation in lowallcitations:
                lowallcitations.append(low_citation)
                if ctype == 'article':
                    articles.append(citation)
                    allcitations.append(citation)
                elif ctype == 'book':
                    books.append(citation)
                    allcitations.append(citation)
                elif ctype == 'incollection':
                    incollections.append(citation)
                    allcitations.append(citation)
                elif ctype == 'misc':
                    miscs.append(citation)
                    allcitations.append(citation)
                else:
                    errors.append(k)
            else:
                duplicates.append(k)
                print('Warning, duplicate: %s' % k)

        print('')

        allcitations.sort()
        for a in allcitations:
            print(a)

        print('')
        print(' %4i entries found' % len(results))
        print(' %4i articles' % len(articles))
        print(' %4i incollections' % len(incollections))
        print(' %4i books' % len(books))
        print(' %4i miscs' % len(miscs))
        print(' %4i errors' % len(errors))
        print(' %4i duplicates' % len(duplicates))
        print('')

        output_log = '%s.log' % os.path.splitext(os.path.basename(ops.output))[0]
        f_out_log = open(output_log, 'w')

        ## write output file, header
        timestamp = time.strftime('%Y-%m-%d-%Hh%M')
        f_out = open(ops.output, 'w')
        f_out.write('## bibtex references file\n')
        f_out.write('## gerenated by markdown_bib.py\n')
        f_out.write('## created: %s\n' % timestamp)
        f_out.write('###############################################################################\n\n')

        ## write lists of the markdown citations to use
        f_out.write('Total Entries: %i\n\n' % len(results))
        f_out_log.write('Total Entries: %i\n\n' % len(results))
        
        f_out.write('Articles: %i\n' % len(articles))
        f_out_log.write('Articles: %i\n' % len(articles))
        for a in articles:
            f_out.write('%s\n' % a)
            f_out_log.write('%s\n' % a)
        f_out.write('\n')
        f_out_log.write('\n')

        f_out.write('Incollections: %i\n' % len(incollections))
        f_out_log.write('Incollections: %i\n' % len(incollections))
        for a in incollections:
            f_out.write('%s\n' % a)
            f_out_log.write('%s\n' % a)
        f_out.write('\n')
        f_out_log.write('\n')

        f_out.write('Books: %i\n' % len(books))
        f_out_log.write('Books: %i\n' % len(books))
        for a in books:
            f_out.write('%s\n' % a)
            f_out_log.write('%s\n' % a)
        f_out.write('\n')
        f_out_log.write('\n')

        f_out.write('Miscs: %i\n' % len(miscs))
        f_out_log.write('Miscs: %i\n' % len(miscs))
        for a in miscs:
            f_out.write('%s\n' % a)
            f_out_log.write('%s\n' % a)
        f_out.write('\n')
        f_out_log.write('\n')

        if errors:
            f_out.write('ERRORS: %i\n' % len(errors))
            f_out_log.write('ERRORS: %i\n' % len(errors))
            for a in errors:
                f_out.write('%s\n' % a)
                f_out_log.write('%s\n' % a)
            f_out.write('\n')
            f_out_log.write('\n')

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
        f_out_log.close()

        print('%s and %s written.' % (ops.output, output_log))
        print('')

#    print('|')
#    print('|  Done!  _______,,,^..^,,,_~_______')
#    print('|')


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
    ops = options()

    reo = rep_incollection.match(line)
    if reo:
        ## parse article
        if ops.verbose:
            print('Incollection: %s' % trim_string(line))
        citation, bibtex = make_incollection(reo)
        return 'incollection', citation, bibtex

    else:
        reo = rep_book.match(line)
        if reo:
            ## parse book
            if ops.verbose:
                print('Book: %s' % trim_string(line))
            citation, bibtex = make_book(reo)
            return 'book', citation, bibtex

        else:
            reo = rep_article.match(line)
            if reo:
                ## parse article
                if ops.verbose:
                    print('Article: %s' % trim_string(line))
                citation, bibtex = make_article(reo)
                return 'article', citation, bibtex

            else:
                reo = rep_misc.match(line)
                if reo:
                    ## parse misc
                    if ops.verbose:
                        print('Misc: %s' % trim_string(line))
                    citation, bibtex = make_misc(reo)
                    return 'misc', citation, bibtex

                else:
                    print('NO MATCH: %s' % trim_string(line))

    return None, None, None


#______________________________________________________________________________
def make_book(reo):
    """
    @book{Author_year_title,
        author      = {},
        year        = {2000},
        title       = {},
        edition     = {2},  # optional
        editor      = {},   # optional
        translator  = {},   # optional
        address     = {},   # optional
        publisher   = "{}",   # optional
        url         = {},   # optional
    }
    """
    lines = []
    cite_author = reo.group('author').split()[0].rstrip(',')
    cite_author_lower = cite_author.lower()
    has_von = False
    if cite_author_lower in ('van', 'von', 'da', 'de', 'di', "'t"):
        cite_author += reo.group('author').split()[1].rstrip(',')
        has_von = True
    cite_year = reo.group('year')
    cite_title = reo.group('title')
    max_title_len = 50
    if len(cite_title) > max_title_len:
        cite_title = textwrap.fill(cite_title, max_title_len).split('\n')[0]
    citation = '%s_%s_%s' % (cite_author, cite_year, cite_title)
    citation = clean_citation(citation)
    lines.append('@book{%s,' % citation)
    author = reo.group('author')
    author = clean_author(author)
    if author.count('Collaboration') or author.count('Lab') or author.count('Corporation') or author.count('et al'):
        lines.append('    author      = "{%s}",' % author)
    else:
        lines.append('    author      = {%s},' % author)
    lines.append('    year        = {%s},' % reo.group('year'))
    lines.append('    title       = "{%s}",' % reo.group('title'))
    if reo.group('edition'):
        lines.append('    edition     = {%s},' % reo.group('edition'))
    if reo.group('editor'):
        editor = reo.group('editor')
        editor = editor.replace(' & ', ' and ')
        lines.append('    editor      = {%s},' % editor)
    if reo.group('translator'):
        translator = reo.group('translator')
        translator = translator.replace(' & ', ' and ')
        lines.append('    translator  = {%s},' % translator)
    if reo.group('address'):
        lines.append('    address     = {%s},' % reo.group('address'))
    if reo.group('publisher'):
        lines.append('    publisher   = "{%s}",' % reo.group('publisher'))
    if reo.group('url'):
        lines.append('    url         = {%s},' % reo.group('url'))
    if reo.group('note'):
        lines.append('    note        = {%s},' % reo.group('note'))
    if has_von:
        lines.append('    options = {useprefix=true},')
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
        publisher   = "{Clarendon Press}",
        address     = {Oxford},
        pages       = {9--23},
        chapter     = {1},
    }
    """
    lines = []
    cite_author = reo.group('author').split()[0].rstrip(',')
    cite_author_lower = cite_author.lower()
    has_von = False
    if cite_author_lower in ('van', 'von', 'da', 'de', 'di', "'t"):
        cite_author += reo.group('author').split()[1].rstrip(',')
        has_von = True
    cite_year = reo.group('year')
    cite_title = reo.group('title')
    max_title_len = 50
    if len(cite_title) > max_title_len:
        cite_title = textwrap.fill(cite_title, max_title_len).split('\n')[0]
    citation = '%s_%s_%s' % (cite_author, cite_year, cite_title)
    citation = clean_citation(citation)
    lines.append('@incollection{%s,' % citation)
    author = reo.group('author')
    author = clean_author(author)
    if author.count('Collaboration') or author.count('Lab') or author.count('Corporation') or author.count('et al'):
        lines.append('    author      = "{%s}",' % author)
    else:
        lines.append('    author      = {%s},' % author)
    lines.append('    year        = {%s},' % reo.group('year'))
    lines.append('    title       = "{%s}",' % reo.group('title'))
    if reo.group('edition'):
        lines.append('    edition     = {%s},' % reo.group('edition'))
    if reo.group('editor'):
        editor = reo.group('editor')
        editor = editor.replace(' & ', ' and ')
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
        lines.append('    publisher   = "{%s}",' % reo.group('publisher'))
    if reo.group('url'):
        lines.append('    url         = {%s},' % reo.group('url'))
    if reo.group('note'):
        lines.append('    note        = {%s},' % reo.group('note'))
    if has_von:
        lines.append('    options = {useprefix=true},')
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
    cite_author_lower = cite_author.lower()
    has_von = False
    if cite_author_lower in ('van', 'von', 'da', 'de', 'di', "'t"):
        cite_author += reo.group('author').split()[1].rstrip(',')
        has_von = True
    cite_year = reo.group('year')
    cite_title = reo.group('title')
    max_title_len = 50
    if len(cite_title) > max_title_len:
        cite_title = textwrap.fill(cite_title, max_title_len).split('\n')[0]
    citation = '%s_%s_%s' % (cite_author, cite_year, cite_title)
    citation = clean_citation(citation)
    lines.append('@article{%s,' % citation)
    author = reo.group('author')
    author = clean_author(author)
    if author.count('Collaboration') or author.count('Lab') or author.count('Corporation') or author.count('et al'):
        lines.append('    author      = "{%s}",' % author)
    else:
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
    if has_von:
        lines.append('    options = {useprefix=true},')
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
    cite_author_lower = cite_author.lower()
    has_von = False
    if cite_author_lower in ('van', 'von', 'da', 'de', 'di', "'t"):
        cite_author += reo.group('author').split()[1].rstrip(',')
        has_von = True
    cite_year = reo.group('year')
    cite_title = reo.group('title')
    max_title_len = 50
    if len(cite_title) > max_title_len:
        cite_title = textwrap.fill(cite_title, max_title_len).split('\n')[0]
    citation = '%s_%s_%s' % (cite_author, cite_year, cite_title)
    citation = clean_citation(citation)
    lines.append('@misc{%s,' % citation)
    author = reo.group('author')
    author = clean_author(author)
    if author.count('Collaboration') or author.count('Lab') or author.count('Corporation') or author.count('et al'):
        lines.append('    author      = "{%s}",' % author)
    else:
        lines.append('    author      = {%s},' % author)
    lines.append('    year        = {%s},' % reo.group('year'))
    lines.append('    title       = "{%s}",' % reo.group('title'))
    if reo.group('howpublished'):
        lines.append('    howpublished = "{%s}",' % reo.group('howpublished'))
    if reo.group('url'):
        lines.append('    url         = {%s},' % reo.group('url'))
    if reo.group('note'):
        lines.append('    note        = {%s},' % reo.group('note'))
    if has_von:
        lines.append('    options = {useprefix=true},')
    lines.append('}')
    s = '\n'.join(lines)
    return citation, s


#______________________________________________________________________________
def clean_citation(s):
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

    ## remove latex \emph
    new_s = new_s.replace('\\emph', '')

    ## remove redundant space (' ' and '_' converted to '-')
    new_s = new_s.replace('     ', ' ')
    new_s = new_s.replace('    ', ' ')
    new_s = new_s.replace('   ', ' ')
    new_s = new_s.replace('  ', ' ')
    new_s = new_s.replace(' ', '-')
    new_s = new_s.replace('_____', ' ')
    new_s = new_s.replace('____', ' ')
    new_s = new_s.replace('___', ' ')
    new_s = new_s.replace('__', ' ')
    new_s = new_s.replace('_', '-')
    new_s = new_s.replace('-----', '-')
    new_s = new_s.replace('----', '-')
    new_s = new_s.replace('---', '-')
    new_s = new_s.replace('--', '-')
    new_s = new_s.replace('.-', '.')
    new_s = new_s.replace('-.', '.')

    ## remove strange characters
    len_fn = len(new_s)
    i = 0
    while i < len_fn:
        ch = new_s[i]
        if not rep_ascii.match(ch): # \w = [a-zA-Z0-9_]
            new_s = new_s.replace(ch, '_')
            len_fn = len(new_s)
        i += 1
    new_s = new_s.replace('_', '')

    ## remove '.'
    new_s = new_s.replace('.', '')

    ## convert all '-' to '_'
    new_s = new_s.replace('-', '_')
    new_s = new_s.strip('_')

    ## chop-off articles
    new_s_lower = new_s.lower()
    if new_s_lower.endswith('_a'):
        new_s = new_s[:-2]
        new_s_lower = new_s.lower()
    if new_s_lower.endswith('_an'):
        new_s = new_s[:-3]
        new_s_lower = new_s.lower()
    if new_s_lower.endswith('_the'):
        new_s = new_s[:-4]
        new_s_lower = new_s.lower()
    ## chop-off prepositions
    if new_s_lower.endswith('_by'):
        new_s = new_s[:-3]
        new_s_lower = new_s.lower()
    if new_s_lower.endswith('_for'):
        new_s = new_s[:-4]
        new_s_lower = new_s.lower()
    if new_s_lower.endswith('_in'):
        new_s = new_s[:-3]
        new_s_lower = new_s.lower()
    if new_s_lower.endswith('_of'):
        new_s = new_s[:-3]
        new_s_lower = new_s.lower()
    if new_s_lower.endswith('_to'):
        new_s = new_s[:-3]
        new_s_lower = new_s.lower()
    if new_s_lower.endswith('_with'):
        new_s = new_s[:-5]
        new_s_lower = new_s.lower()
    ## chop-off conjuctions
    if new_s_lower.endswith('_and'):
        new_s = new_s[:-4]
        new_s_lower = new_s.lower()

    return new_s


#______________________________________________________________________________
def clean_author(s):
    """
    Ladyman, J., Ross, D., Spurrett, D., & Collier, J.

    words = s.split()
    for word in words:
        pass

    TODO: Put spaces between each initial.
    TODO: Put and's between each author.
    s = s.replace('&', 'and')
    """
    if s.startswith('{'):
        return s
    reo = rep_author.search(s)
    if reo:
        if reo.group('etal'):
            assert reo.group('a1')
#            s = '%s and others' % reo.group('a1')
#            s = '%s \\emph{et al}.' % reo.group('a1')
            s = '%s et al.' % reo.group('a1')
        elif reo.group('a6'):
            assert reo.group('a1')
#            s = '%s and others' % reo.group('a1')
#            s = '%s \\emph{et al}.' % reo.group('a1')
            s = '%s et al.' % reo.group('a1')
        elif reo.group('a5'):
            assert reo.group('a1')
#            s = '%s and others' % reo.group('a1')
#            s = '%s \\emph{et al}.' % reo.group('a1')
            s = '%s et al.' % reo.group('a1')
        else:
            authors = []
            if reo.group('a1'):
                authors.append(reo.group('a1'))
            if reo.group('a2'):
                authors.append(reo.group('a2'))
            if reo.group('a3'):
                authors.append(reo.group('a3'))
            if reo.group('a4'):
                authors.append(reo.group('a4'))
            if reo.group('a5'):
                authors.append(reo.group('a5'))
            new_authors = []
            for a in authors:
                newa =    a.replace('.', '. ')
                newa = newa.replace('  ', ' ')
                newa = newa.strip()
                new_authors.append(newa)
            s = ' and '.join(new_authors)
    return s


#______________________________________________________________________________
def check_for_url(s=''):
    reo = rep_url.search(s)
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
    print(line)
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
