Getting started
===============================================================================

<!-- PAGETOC -->


Checking-out the template
-------------------------------------------------------------------------------

Checking out markdown-memo with a simple git command, like:

    git clone https://github.com/rreece/markdown-memo.git

TODO: discuss the [README.md](https://github.com/rreece/markdown-memo/blob/master/README.md).


Starting a page or section
-------------------------------------------------------------------------------

Just open or create a first `md` file in that directory like `01-introduction.md`,
and start typing.
Each file should probably correspond to a webpage or section in the document,
and in that case, it should begin with an `h1`-level heading (section), denoted with
a double-rule of equal-signs, like:

    Section title
    ===============================================================================

Or marked like this:

    # Section title

Then you can have sub-sections as you wish, and/or just start typing the main text.
There's no need for additional markup or html.


Going from there
-------------------------------------------------------------------------------

The following sections of this example document will show examples of
Markdown syntax.
For now, briefly, examples of [Markdown](http://daringfireball.net/projects/markdown/)
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


Building your document
-------------------------------------------------------------------------------

In addition to writing the basic `md` files for your project, you need to write
a metadata file: `meta.yaml`.  See the example metadata there.

Then you can build your document.
A lot of the inner-workings of `markdown-memo` are done in the `Makefile`.

-   Call `make` to generate valid xhtml.
-   Call `make pdf` to generate a pdf document.
-   Call `make clean` to delete temporary LaTeX files.
-   Call `make realclean` to additionally delete the output html and pdf files.

I use an image of my email to hide it from text crawlers.
Please replace `img/my_email.png` with a screenshot of your
email address instead of mine,
or just remove the use of the image in `meta.yaml`.

Customize the files in `templates/` to adjust the format
of the output html and pdfs files to your needs.


