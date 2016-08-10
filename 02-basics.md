Basics
===============================================================================

Subsection
-------------------------------------------------------------------------------

URLs are done like the following.

[Lorem ipsum](https://en.wikipedia.org/wiki/Lorem_ipsum)
dolor sit amet, duo ut putant verear, nam ut brute utroque.
Officiis qualisque conceptam te duo, eu vim soluta numquam, has ut aliquip
accusamus. Probo aliquam pri id. Mutat singulis ad vis, eam euismod pertinax
an, ea tale volumus vel. At porro soleat est. Debet facilis admodum an sed,
at falli feugiat est.

### Blocks

Unnumbered lists like this:

-   Galileo Galilei
-   Robert G. Ingersoll
-   Jill Tarter

Numbered lists like this:

1.  Na&iuml;ve realists
1.  Scientific realists
1.  Constructive empiricists
1.  Positivists
1.  Relativists

The following is a quote block. 

>   It ain't what you don't know that gets you into trouble. It's what you know for sure that just ain't so.  

-- Mark Twain

The following is a code block.

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

Maybe you want to refer to code inline like this: `vec.push_back(3.14)`.


### Fonts

-   *This is emphasis.*
-   **This is bold.**
-   _This is also emphasis._
-   __This is also bold.__
-   ~~This is struck-out.~~

These will work in LaTeX (\LaTeX) but may not in html:

-   \textsf{This should be Sans.}
-   \textsc{This Should BE SMALL caps.}
-   $\textsf{This works though!}$
-   $\textsc{But this does not!}$



Footnotes and citations.
-------------------------------------------------------------------------------

Here's how you do footnotes.
Let's get real[^Miller2014].
Let's try citing various kinds of references.
Feynman said some important things[^Feynman1963].
But everything is a footnote to Plato[^Plato2000].
Quine[^Quine1969] and Van[^vanFraassen1980] are cool cats too.

[^Feynman1963]: @Feynman_1963_The_Feynman_Lectures_on_Physics_Volume_I\, ch. 3.

[^Feynman1965]: @Feynman_1965_The_Development_of_the_Space_Time_View_of_Quantum\.

[^Miller2014]: @Miller_2014_Realism\. See also "[Philosophical realism](https://en.wikipedia.org/wiki/Philosophical_realism)" - Wikipedia.

[^Plato2000]: @Plato_2000_The_Republic\.

[^Quine1969]: @Quine_1969_Natural_kinds\.

[^vanFraassen1980]: @vanFraassen_1980_The_Scientific_Image\.



