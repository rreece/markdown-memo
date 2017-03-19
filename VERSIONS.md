v0.29  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   March 19, 2017
-   new JHEP template

v0.28  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   March 1, 2017
-   fixes in make_bib_index.py

v0.27  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   March 1, 2017
-   color fixes in email images
-   This version is finally looking pretty polished.

v0.26  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   February 28, 2017
-   bugfix in markdown2bib.py
-   links now underline only on hover

v0.25  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   February 28, 2017
-   Conclusions -> Conclusion
-   Shrinked footnote size to 14px
-   markdown2bib.py fixes for et al.

v0.24  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   February 24, 2017
-   More css improvements.
-   Shared on twitter.

v0.23  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   February 24, 2017
-   Some css and html template cleanup.

v0.22  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   February 16, 2017
-   Fixed bugs in wordcount, was line count.
-   Word-count and page-count now printed at the end of make pdf.

v0.21  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   January 24, 2017
-   Lot's of fixes to multiple authors and other things.

v0.20  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   September 4, 2016
-   apa-no-doi-no-issue-with-notes.csl now has
    subsequent-author-substitute="&#8212;&#8212;&#8212;"
    subsequent-author-substitute-rule="complete-all"

v0.19  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   September 3, 2016
-   Added favicon support. Social media thumbnail still doesn't work.
-   Updated documentation some.

v0.18  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   August 28, 2016
-   Updated documentation some.

v0.17  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   August 27, 2016
-   Updated documentation some.
-   Some bugfixes to scripts.

v0.16  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   August 27, 2016
-   Added scripts/transform_html.py
-   Wrote a script to generate a md file with footnotes and citations defined given a bibliography (`make_bib_index.py`).
-   Find and replaces such that LaTeX figures use pdf figures while html uses raster png/jpg.
-   Optionally makes a TOC automatically in the html. (transform_html.py)
-   Makes links to previous and next sections (if they exist) in the navigation box in the html. (transform_html.py)

v0.15  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   August 11, 2016
-   Added `markdown-memo-alt.css`
-   css now configurable in `meta.yaml`
-   Lots of fixes in templates/*.html

v0.14  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   August 10, 2016
-   Some updates to the `README.md` and the examples.

v0.13  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   August 10, 2016
-   Fixed image widths and heights
-   When making a pdf, jpg/png figures automatically get replaced with pdf
    figures if they exist.

v0.12  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   August 9, 2016
-   Split templates/ and into templates/ and scripts/.

v0.11  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   August 9, 2016
-   A million fancy improvements
-   references section only when needed in html
-   wordcount

v0.10  Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   March 16, 2016
-   Added templates/refs_tex.md and templates/*.csl
-   Updated to use APA citation formats.
-   Shrank the TOC and Refs spacing.
-   Sans-serif quote blocks, etc., looking a lot more polished.

v0.9   Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   March 6, 2016
-   Added templates/refs_subsection.md

v0.8   Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   March 6, 2016
-   Added use of pandoc-crossref
-   Lots of polishing of templates
-   Lot's of new syntax examples in the *.md

v0.6/7   Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   Feb 27, 2016
-   Lots of updates including getting the abstract into the html.

v0.5    Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   Clean-up of example*.md
-   Some updates to markdown-memo.css

v0.4    Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   Jan 23, 2016
-   Updates to markdown-memo.css
-   Several fixes to html templates. Now validates.

v0.3    Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   August 7, 2015
-   Forgot a commit before tagging.

v0.2    Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   August 7, 2015
-   Many major changes including bibliography and disqus integration.

v0.1    Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   added LICENSE option to the Makefile

v0.0    Ryan Reece  <ryan.reece@cern.ch>
----------------------------------
-   first release

