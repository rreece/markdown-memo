markdown-memo
=============

This package makes it very easy to compile notes taken in
[Markdown](http://daringfireball.net/projects/markdown/)
to valid xhtml or to a pdf via LaTeX.

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

