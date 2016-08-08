markdown-memo
===========================

This package makes it very easy to compile notes taken in
[Markdown](http://daringfireball.net/projects/markdown/)
to valid xhtml or to a pdf via LaTeX.
It can be used to make simple webpages quickly,
for example, [rreece.github.io/sw](http://rreece.github.io/sw/).

-   author:  Ryan Reece <ryan.reece@cern.ch>
-   created: July 29, 2014


Requirements
----------------------------------

-   LaTeX
-   pandoc
-   make

I've also had to install `pandoc-crossref`, and I think I had to install `pandoc-citeproc`.
In the case of [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref), you simply
do this to install:

    cabal update
    cabal install pandoc-crossref


Getting started
----------------------------------

-   Clone/fork this package and possibly rename the `markdown-memo`
    directory as your project.
-   Put some `*.md` files in that directory.
-   In those files, just start writing the `h1` heading.
    There's no need for additional markup or html.
    Examples of [Markdown](http://daringfireball.net/projects/markdown/)
    syntax are

        Section 1
        =================================

        Sub-section 1
        ---------------------------------

        [Lorem ipsum](https://en.wikipedia.org/wiki/Lorem_ipsum)
        dolor sit amet, duo ut putant verear, nam ut brute utroque.
        Officiis qualisque conceptam te duo, eu vim soluta numquam, has ut aliquip
        accusamus. Probo aliquam pri id. Mutat singulis ad vis, eam euismod pertinax
        an, ea tale volumus vel. At porro soleat est. Debet facilis admodum an sed,
        at falli feugiat est.

        1.  one
        1.  two
        1.  three
    
        You can do latex in-line, $e^{i\pi} + 1 = 0$, like that.
        Or equations:

        \begin{equation}
            \int_{\partial\Omega} \omega = \int_{\Omega} \mathrm{d}\omega \,.
        \end{equation}


-   Edit the metadata in `meta.yaml`.
-   Call `make` to generate a pdf document.
-   Call `make html` to generate valid xhtml.

I use an image of my email to hide it from text crawlers.
Please replace `img/my_email.png` with a screenshot of your
email address instead of mine,
or just remove the use of the image in `meta.yaml`.

Customize the files in `templates/` to adjust the format
of the output html and pdfs files to your needs.

If you want to put the html online, perhaps a solution for you,
because it's free and easy, would be to host the pages at github.
See: [pages.github.com](https://pages.github.com/).


Features
----------------------------------

### html

-   [disqus comments](disqus.com)
-   mathjax LaTeX rendering
-   google analytics tracking
-   automatically generates an `index.md`

If you want to write your own `index.md`,
then put the same markdown in `index.txt`.

### pdf

-   LaTeX
-   fancyheader

### both

-   appendices
-   bibtex bibliographies
-   footnotes
-   multiple authors
-   word- and page-count plots (see below)

If you add multiple appendices, perhaps you want to separate
them from the main text with a part:

    \clearpage
    \appendix
    \part*{Appendices}
    \addcontentsline{toc}{part}{Appendices}

    Example appendix
    ===============================================================================

    Start writing the appendix...
    


Disqus integration
----------------------------------

You can choose to append a comments section at the end of your html.
Just register a user name and the site name with [disqus.com](disqus.com).
Then in the `meta.yaml`, set `disqus: true`, and set your `disqus_shortname`.


Word count
----------------------------------

Note that word-count and page-count plots are generated when you call make.
You might want to keep these around in the `README.md` for your document.

![my pages](wordcount/pages.png)

![my words](wordcount/words.png)


Wish list / TODOs
----------------------------------

-   ~~Optionally make a TOC automatically in the html.~~
-   ~~Find and replace the default figure environment to be `\begin{figure}[tph]` instead of `\begin{figure}[htbp]`.~~
-   ~~Add conditionals to the `Makefile` such that `templates/refs.md` is only added for documents that have references.~~
-   Find and replace such that LaTeX figures use pdf figures while html uses raster png/jpg.
-   Get tables to be normal `\begin{table}[bph]` instead of the `longtable` environment.


See also
----------------------------------

-   [rreece.github.io/sw](http://rreece.github.io/sw/)
-   [kprussing.github.io/writing-with-markdown](http://kprussing.github.io/writing-with-markdown/)
-   [programminghistorian.org/lessons/sustainable-authorship-in-plain-text-using-pandoc-and-markdown](http://programminghistorian.org/lessons/sustainable-authorship-in-plain-text-using-pandoc-and-markdown)
-   [pandoc.org/README.html](http://pandoc.org/README.html)
-   [commonmark.org](http://commonmark.org/)
-   [scholarlymarkdown.com](http://scholarlymarkdown.com/)
-   [github.com/lierdakil/pandoc-crossref](https://github.com/lierdakil/pandoc-crossref)


