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


Lists
-------------------------------------------------------------------------------

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


Blocks
-------------------------------------------------------------------------------

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


Fonts
-------------------------------------------------------------------------------

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


Links
-------------------------------------------------------------------------------

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


