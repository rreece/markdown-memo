markdown-memo
=============

This package makes it very easy to use [pandoc](http://johnmacfarlane.net/pandoc/)
to compile notes taken in
[Markdown](http://daringfireball.net/projects/markdown/)
into valid xhtml or to a pdf via LaTeX.
It basically consists of a Makefile and some html/css templates.

-   author:  Ryan Reece <ryan.reece@cern.ch>
-   created: July 29, 2014

Requirements
----------------------------------

-   LaTeX
-   pandoc
-   make


Getting started
----------------------------------

-   Clone/fork this package and possibly rename the `markdown-memo`
    directory as your project.
-   Put some `*.md` files in that directory.
-   In those files, just start writing the `h1` heading.
    There's no need for additional markup or html.


        Chapter
        =================================

        Section 1
        ---------------------------------

        Blah blah blah.

        1.  one
        1.  two
        1.  three


-   Edit the `AUTHOR` and `HEADER` variables in the `Makefile`.
-   Call `make` to generate valid xhtml.
-   Call `make pdf` to generate pdf documents.


License
----------------------------------

-   Copyright 2014-2015 The authors
-   License: GPL <http://www.gnu.org/licenses/gpl.html>


