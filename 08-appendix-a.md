\appendix

Special features
===============================================================================

This is an appendix.

If you add multiple appendices, perhaps you want to separate them from the main text with a part:

    \clearpage
    \appendix
    \part*{Appendices}
    \addcontentsline{toc}{part}{Appendices}
    
    Example appendix
    ===============================================================================
    
    Start writing the appendix...


Disqus integration
-------------------------------------------------------------------------------

You can choose to append a comments section at the end of your html.
Just register a user name and the site name with [disqus.com](disqus.com).
Then in the `meta.yaml`, set `disqus: true`, and set your `disqus_shortname`.


Word count
-------------------------------------------------------------------------------

Note that word-count and page-count plots are generated when you call `make pdf`.
You might want to keep these around in the `README.md` for your document.

![my pages](wordcount/pages.png)

![my words](wordcount/words.png)


