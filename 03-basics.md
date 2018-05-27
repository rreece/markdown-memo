Markdown basics
===============================================================================

Here we review the basics of Markdown.
A further reference on Markdown syntax by its creator is
[here](http://daringfireball.net/projects/markdown/syntax).

<!-- PAGETOC -->

Sections {#sec:sections}
-------------------------------------------------------------------------------

Are markded like this:

    Section title {#sec:put-optional-section-label-here}
    ===============================================================================

    Sub-section title {#sec:put-optional-sub-section-label-here}
    -------------------------------------------------------------------------------


Or marked like this:

    # Section title {#sec:put-optional-section-label-here}

    ## Sub-section title {#sec:put-optional-sub-section-label-here}
 
    ### Sub-sub-section title

    Main text here.

Note the examples of labeling a section in braces with `#`, as shown above.
This allows one to refer to labels in the text like:

    The next section, [@sec:lists], is about lists.

The next section, [@sec:lists], is about lists.


Lists {#sec:lists}
-------------------------------------------------------------------------------

**Unnumbered lists** like this:

    -   Galileo Galilei
    -   Robert G. Ingersoll
    -   Jill Tarter

-   Galileo Galilei
-   Robert G. Ingersoll
-   Jill Tarter

**Numbered lists** like this:

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


Blocks {#sec:blocks}
-------------------------------------------------------------------------------

The following is a **quote block**. 

    >   It ain't what you don't know that gets you into trouble.
    >   It's what you know for sure that just ain't so.  

    -- Mark Twain

>   It ain't what you don't know that gets you into trouble.
>   It's what you know for sure that just ain't so.  

-- Mark Twain

A **code block** (used throughout these examples) is just indented with 4 spaces, like this:

        def bubble_sort(alist):
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
        bubble_sort(alist)
        print(alist)

which makes:

    def bubble_sort(alist):
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
    bubble_sort(alist)
    print(alist)

Maybe you want to refer to **code inline** like this with backticks:

    Here's some inline code: `vec.push_back(3.14)`.

Here's some inline code: `vec.push_back(3.14)`.

For poems and the like where you want **linebreaks taken literally**,
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

Otherwise, one can put two or more spaces at the end of a line of Markdown
for the linebreak to be taken literally  
like  
this.

A **horizontal rule** can be made by just writing some number of dashes:

    ----------------------------------------------------

----------------------------------------------------

Boom.


Fonts {#sec:fonts}
-------------------------------------------------------------------------------

    -   *This is emphasis.*
    -   **This is bold.**
    -   _This is also emphasis._
    -   __This is also bold.__
    -   _This is emphasis **and** bold._
    -   __This is bold *and* emphasis.__
    -   ~~This is struck-out.~~

produces:

-   *This is emphasis.*
-   **This is bold.**
-   _This is also emphasis._
-   __This is also bold.__
-   _This is emphasis **and** bold._
-   __This is bold *and* emphasis.__
-   ~~This is struck-out.~~

Don't do these. These will work in LaTeX (\LaTeX) but may not in html.

    -   \textsf{This should be Sans.}
    -   \textsc{This Should BE SMALL caps.}
    -   $\textsf{This works though!}$
    -   $\textsc{But this does not!}$


Links and labels {#sec:links-and-labels}
-------------------------------------------------------------------------------

Links to URLs are done like this:

    [Lorem ipsum](https://en.wikipedia.org/wiki/Lorem_ipsum)

[Lorem ipsum](https://en.wikipedia.org/wiki/Lorem_ipsum)

or used directly like this:

    <https://www.google.com>

<https://www.google.com>

When referring to labeled sections/figures/tables,
you do not include the literal word "Section", "Figure", or "Table",
which will be included for you.
These prefixes/words are configurable in the `meta.yaml` file.

Refer to labeled things like this:

-   **for sections:** `See [@sec:footnotes] on footnotes.`     
    See [@sec:footnotes] on footnotes.
-   **for figures:** `[@fig:scientific_universe] motivates the unity of science.`         
    [@fig:scientific_universe] motivates the unity of science.
-   **for tables:** `Numbers are in [@tbl:atlas_channels].`        
    Numbers are in [@tbl:atlas_channels].
-   **for equations:** `The generalized Stokes' theorem, [@eq:stokes], is rad.`          
    The generalized Stokes' theorem, [@eq:stokes], is rad.

TODO: The above references to labels on other pages unfortunately don't work in html,
but they work in latex/pdf.

You can refer to multiple lables like [@sec:sections;@sec:lists;@sec:blocks] like this:

    [@sec:sections;@sec:lists;@sec:blocks]

Automatic grouping into a range doesn't seem to be working (for latex, but does for html),
so you can also try refer to [Sections @sec:sections]--[-@sec:blocks]
in some versions like this:

    [Sections @sec:sections]--[-@sec:blocks]
    

Footnotes {#sec:footnotes}
-------------------------------------------------------------------------------

    Here's how you do a footnote[^SomeSpecialNote].

    [^SomeSpecialNote]: Lorem ipsum dolor sit amet, duo ut putant verear, nam ut brute utroque.
        Officiis qualisque conceptam te duo, eu vim soluta numquam, has ut aliquip
        accusamus. Probo aliquam pri id. Mutat singulis ad vis, eam euismod pertinax
        an, ea tale volumus vel. At porro soleat est. Debet facilis admodum an sed,
        at falli feugiat est.

produces:

Here's how you do a footnote[^SomeSpecialNote].

[^SomeSpecialNote]: 
    Lorem ipsum dolor sit amet, duo ut putant verear, nam ut brute utroque.
    Officiis qualisque conceptam te duo, eu vim soluta numquam, has ut aliquip
    accusamus. Probo aliquam pri id. Mutat singulis ad vis, eam euismod pertinax
    an, ea tale volumus vel. At porro soleat est. Debet facilis admodum an sed,
    at falli feugiat est.

