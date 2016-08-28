Introduction
===============================================================================


What this is for
-------------------------------------------------------------------------------

TODO: explain the vision.

-   Explain the use cases.


How it works
-------------------------------------------------------------------------------

-   Explain [markdown](https://daringfireball.net/projects/markdown/).
-   Explain [pandoc](http://pandoc.org/).
-   Explain [markdown-memo](https://github.com/rreece/markdown-memo).


**Keep content and style separated**

The idea is that all user *content* should be in plainly written `*.md` files
and one metadata file: `meta.yaml`.
All *stylistic* issues should be implemented in the details of the files
in `templates/` and configurable through `meta.yaml`

For example, see what changes when this document is created with

    css: 'templates/markdown-memo-alt.css'

set in `meta.yaml`, instead of the [default](http://rreece.github.io/sw/markdown-memo/01-introduction.html).
`'templates/markdown-memo.css'`,
as is [shown here](http://rreece.github.io/sw/markdown-memo-alt/01-introduction.html).

