Bibliographies
===============================================================================

<!-- PAGETOC -->

Making a bibliography
-------------------------------------------------------------------------------

TODO.


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

In order for a References section to be generated per-html-page, you need to
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


