markdown-memo
===========================

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

        Section 1
        =================================

        Sub-section 1
        ---------------------------------

        Blah blah blah.

        1.  one
        1.  two
        1.  three

-   Edit the metadata in `meta.yaml`. Example licenses are
-   Call `make` to generate valid xhtml.
-   Call `make pdf` to generate pdf documents.

I use an image of my email to hide it from text crawlers.
Please replace `img/my_email.png` with a screenshot of your
email address instead of mine,
or remove the use of the image in `meta.yaml`.

Customize the files in `templates/` to ajust the format
of the output html and pdfs files to your needs.

If you want to put the html online, perhaps a solution for you,
because it's free and easy, would be to host the pages at github.
See: [pages.github.com](https://pages.github.com/).


Disqus integration
----------------------------------

You can choose to append a comments section at the end of your html.
Just register a user name and the site name with [disqus.com](disqus.com).
Then in the `meta.yaml`, set `disqus: true`, and set your `disqus_shortname`.


See also
----------------------------------

-   [kprussing.github.io/writing-with-markdown](http://kprussing.github.io/writing-with-markdown/)
-   [programminghistorian.org/lessons/sustainable-authorship-in-plain-text-using-pandoc-and-markdown](http://programminghistorian.org/lessons/sustainable-authorship-in-plain-text-using-pandoc-and-markdown/)
-   [pandoc.org/README.html](http://pandoc.org/README.html)
-   [commonmark.org](http://commonmark.org/)


