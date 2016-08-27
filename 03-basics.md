Markdown basics
===============================================================================

<!-- PAGETOC -->


Sections
-------------------------------------------------------------------------------

Are markded like this:

    Section title
    ===============================================================================

    Sub-section title
    -------------------------------------------------------------------------------


Or marked like this:

    # Section title

    ## Sub-section title
 
    ### Sub-sub-section title

    Main text here.


Basic typesetting
-------------------------------------------------------------------------------


### Lists

Unnumbered lists like this:

    -   Galileo Galilei
    -   Robert G. Ingersoll
    -   Jill Tarter

-   Galileo Galilei
-   Robert G. Ingersoll
-   Jill Tarter

Numbered lists like this:

    1.  Na&iuml;ve realists
    1.  Scientific realists
    1.  Constructive empiricists
    1.  Positivists
    1.  Relativists

1.  Na&iuml;ve realists
1.  Scientific realists
1.  Constructive empiricists
1.  Positivists
1.  Relativists

### Blocks

The following is a quote block. 

    >   It ain't what you don't know that gets you into trouble.
    >   It's what you know for sure that just ain't so.  

    -- Mark Twain

>   It ain't what you don't know that gets you into trouble.
>   It's what you know for sure that just ain't so.  

-- Mark Twain

A code block (used throughout these examples) is just indented with 4 spaces, like this:

        def shortBubbleSort(alist):
            exchanges = True
            passnum = len(alist)-1
            while passnum > 0 and exchanges:
               exchanges = False
               for i in range(passnum):
                   if alist[i]>alist[i+1]:
                       exchanges = True
                       temp = alist[i]
                       alist[i] = alist[i+1]
                       alist[i+1] = temp
               passnum = passnum-1
    
        alist=[20,30,40,90,50,60,70,80,100,110]
        shortBubbleSort(alist)
        print(alist)

which makes:

    def shortBubbleSort(alist):
        exchanges = True
        passnum = len(alist)-1
        while passnum > 0 and exchanges:
           exchanges = False
           for i in range(passnum):
               if alist[i]>alist[i+1]:
                   exchanges = True
                   temp = alist[i]
                   alist[i] = alist[i+1]
                   alist[i+1] = temp
           passnum = passnum-1
    
    alist=[20,30,40,90,50,60,70,80,100,110]
    shortBubbleSort(alist)
    print(alist)

Maybe you want to refer to code inline like this with backticks:

    Here's some inline code: `vec.push_back(3.14)`.

Here's some inline code: `vec.push_back(3.14)`.

For poems and the like where you want linebreaks taken literally,
prepend lines with `|` and a single space.  Additional spaces
can be used, but will indent the output.

    | Art is long,
    | Life is short,
    | Opportunity fleeting,
    | Experiment dangerous,
    | Judgment difficult.

| Art is long,
| Life is short,
| Opportunity fleeting,
| Experiment dangerous,
| Judgment difficult.


### Fonts

    -   *This is emphasis.*
    -   **This is bold.**
    -   _This is also emphasis._
    -   __This is also bold.__
    -   ~~This is struck-out.~~

produces:

-   *This is emphasis.*
-   **This is bold.**
-   _This is also emphasis._
-   __This is also bold.__
-   ~~This is struck-out.~~

Don't do this. These will work in LaTeX (\LaTeX) but may not in html.

    -   \textsf{This should be Sans.}
    -   \textsc{This Should BE SMALL caps.}
    -   $\textsf{This works though!}$
    -   $\textsc{But this does not!}$

produces:

-   \textsf{This should be Sans.}
-   \textsc{This Should BE SMALL caps.}
-   $\textsf{This works though!}$
-   $\textsc{But this does not!}$


### Links

URLs are done like this:

    [Lorem ipsum](https://en.wikipedia.org/wiki/Lorem_ipsum)

[Lorem ipsum](https://en.wikipedia.org/wiki/Lorem_ipsum)

To reference

-   equation: `eq.\ $\eqref{eq:stokes}$`    
    eq.\ $\eqref{eq:stokes}$
-   figure: `[@Fig:scientific_universe]`    
    [@Fig:scientific_universe]
-   table: `[@Tbl:atlas_channels]`    
    [@Tbl:atlas_channels]
-   section: `[@sec:footnotes-and-citations]`    
    [@sec:footnotes-and-citations]


Footnotes and citations {#sec:footnotes-and-citations}
-------------------------------------------------------------------------------

    Here's how you do a footnote[^SomeSpecialNote].

    [^SomeSpecialNote]: Lorem ipsum dolor sit amet, duo ut putant verear, nam ut brute utroque.
        Officiis qualisque conceptam te duo, eu vim soluta numquam, has ut aliquip
        accusamus. Probo aliquam pri id. Mutat singulis ad vis, eam euismod pertinax
        an, ea tale volumus vel. At porro soleat est. Debet facilis admodum an sed,
        at falli feugiat est.

produces:

Here's how you do a footnote[^SomeSpecialNote].

[^SomeSpecialNote]: Lorem ipsum dolor sit amet, duo ut putant verear, nam ut brute utroque.
    Officiis qualisque conceptam te duo, eu vim soluta numquam, has ut aliquip
    accusamus. Probo aliquam pri id. Mutat singulis ad vis, eam euismod pertinax
    an, ea tale volumus vel. At porro soleat est. Debet facilis admodum an sed,
    at falli feugiat est.

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


[^Feynman1963]: @Feynman_1963_The_Feynman_Lectures_on_Physics_Volume_I\, ch. 3.

[^Feynman1965]: @Feynman_1965_The_Development_of_the_Space_Time_View_of_Quantum\.

[^Miller2014]: @Miller_2014_Realism\. See also "[Philosophical realism](https://en.wikipedia.org/wiki/Philosophical_realism)" - Wikipedia.

[^Plato2000]: @Plato_2000_The_Republic\.

[^Quine1969]: @Quine_1969_Natural_kinds\.

[^vanFraassen1980]: @vanFraassen_1980_The_Scientific_Image\.



