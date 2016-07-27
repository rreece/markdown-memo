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



Footnotes
-------------------------------------------------------------------------------

Here's how you do footnotes. Lorem ipsum[^Realism]
dolor sit amet, duo ut putant verear, nam ut brute utroque.
Officiis qualisque conceptam te duo, eu vim soluta numquam, has ut aliquip
accusamus. Probo aliquam pri id. Mutat singulis ad vis, eam euismod pertinax
an, ea tale volumus vel. At porro soleat est. Debet facilis admodum an sed,
at falli feugiat est[^Feynman].

[^Realism]: @Miller_2014_realism\. See also "[Philosophical realism](https://en.wikipedia.org/wiki/Philosophical_realism)" - Wikipedia.
[^Feynman]: @Feynman_1963_feynman_lectures_vol1_ch3\.

Ne nonumy quodsi petentium vix, mel ad errem accusata periculis. Porro
urbanitas consetetur mei eu, his nisl officiis ei. Ei cum fugit graece,
ne qui tantas qualisque voluptaria. Vis ut laoreet euripidis, vix aeque
omittam at, vix no cetero volumus. Per te omnium volutpat torquatos, cu vis
sumo decore. Eirmod hendrerit an pri.


Amet magna voluptatum eam eu. Denique moderatius ad pri, an vix tale
referrentur, atqui appetere et eos. Pri esse disputationi et. Te his
assum persius, in eam deterruisset consequuntur. Quando signiferumque no
his, usu nusquam corrumpit ex, sea ex soluta option facilisis. Ne autem
assentior consequuntur nam, constituto scripserit no eam. Eu laoreet
fabellas postulant eos.


