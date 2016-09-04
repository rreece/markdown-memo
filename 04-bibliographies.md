Bibliographies
===============================================================================

<!-- PAGETOC -->

Making a bibliography
-------------------------------------------------------------------------------

Markdown-memo uses [bibtex](https://en.wikipedia.org/wiki/BibTeX) 
via [pandoc](http://pandoc.org/) to generate a bibliography for your document.
We've made this even simpler by allowing the user to create a simple text
file to generate the necessary bibtex `.bib` file using the
[`markdown2bib`](https://github.com/rreece/markdown2bib) script.
Markdown-memo looks for any `bibs/*.txt` files and uses `markdown2bib`
to combine them and create `bibs/mybib.bib` in bibtex format.
This is later used by pandoc when creating tex $\rightarrow$ pdf
or html.

The `bibs/*.txt` should be plain text with a single reference per line,
with each reference in a style that loosely follows the
[American Psychological Association (APA)](http://www.library.arizona.edu/search/reference/citation-apa.html),
which is commonly used in humanities.
Currently four types of references are supported: `article`, `book`, `incollection`, and `misc`.
The journal or book titles need to be in markdown-style emphasis, meaning `*Set Within Asterixis*`. 

For example, the `mybib.txt` file in this document is

    ATLAS Collaboration. (2008). The ATLAS Experiment at the CERN Large Hadron Collider. *JINST*, 3, S08003.
    ATLAS Collaboration. (2012). Observation of a new particle in the search for the Standard Model Higgs boson with the ATLAS detector at the LHC. *Phys.Lett.*, B716, 1--29.
    Feynman, R.P. (1963). *The Feynman Lectures on Physics, Volume I*. California Institute of Technology. http://www.feynmanlectures.caltech.edu/I_03.html
    Feynman, R.P. (1965). The Development of the Space-Time View of Quantum Electrodynamics. Nobel Lecture, December 11, 1965. http://www.nobelprize.org/nobel_prizes/physics/laureates/1965/feynman-lecture.html
    Miller, A. (2014). Realism. *Stanford Encyclopedia of Philosophy*. http://plato.stanford.edu/entries/realism/
    Plato. (2000). *The Republic*. (G. Ferrari, Ed. & T. Griffith, Trans.). Cambridge: Cambridge University Press. [(Originally written ca. 380 BCE.)]
    Quine, W.V.O. (1969). Natural kinds. In *Ontological Relativity and Other Essays*. New York: Columbia University Press.
    van Fraassen, B. (1980). *The Scientific Image*. Oxford: Oxford University Press.

If you do not need a bibliography, set

    dorefs: false

in `meta.yaml`, and then these scripts and programs are not run.


Doing citations
-------------------------------------------------------------------------------

Citations start with an `@`-sign, and can be used inline, like:

    @Miller_2014_Realism argues that we should get real.

which produces:

@Miller_2014_Realism argues that we should get real.

Inside a caption, you may want to end it with the citation in parentheses
like this:

    Blah blah blah [@Feynman_1963_The_Feynman_Lectures_on_Physics_Volume_I]\.

which produces:

Blah blah blah [@Feynman_1963_The_Feynman_Lectures_on_Physics_Volume_I]\.

Typically, I find it better to leave citations[^Quine1969] in footnotes to keep from
cluttering the main text.
Let's try citing various kinds of references.
Feynman said some important things[^Feynman1965].
But everything is a footnote to Plato[^Plato2000].
Van[^vanFraassen1980] is a cool cat too.

In order for a References section to be generated per html page, you need to
add a special html comment near the end of your Markdown file for that page:

    <!-- REFERENCES -->

Pages without such a comment will not get an automatic References section,
but the complete pdf document will automatically still have a complete References
section at the end as long as

    dorefs: true

is set in `meta.yaml`.



[^Feynman1963]: @Feynman_1963_The_Feynman_Lectures_on_Physics_Volume_I\, ch. 3.

[^Feynman1965]: @Feynman_1965_The_Development_of_the_Space_Time_View_of_Quantum\.

[^Miller2014]: @Miller_2014_Realism\. See also "[Philosophical realism](https://en.wikipedia.org/wiki/Philosophical_realism)" - Wikipedia.

[^Plato2000]: @Plato_2000_The_Republic\.

[^Quine1969]: @Quine_1969_Natural_kinds\.

[^vanFraassen1980]: @vanFraassen_1980_The_Scientific_Image\.


<!-- REFERENCES -->


