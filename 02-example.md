Section 2
===============================================================================

Subsection 2.1
-------------------------------------------------------------------------------

What am I doing?

Here we show that you can integrate LaTeX equations right in the
middle of markdown. This is some math.

\begin{align}
    x&=1 \label{eq:1}\\
    y&=2
\end{align}

Some text.

\begin{equation}
    e^{i\pi} + 1 = 0
\end{equation}

You can also refer to labeled equations, such as $\eqref{eq:1}$.

Stokes' theorem is pretty cool:

\begin{equation}
    \int_{\partial\Omega} \omega = \int_{\Omega} \mathrm{d}\omega \,.
\end{equation}

Note that we are using [MathJax](https://www.mathjax.org/) to render
the equations in html. Our html template includes the following code
to ask MathJax to render it and number the equations:

    <!--- MathJax stuff -->
    <script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({ TeX: { equationNumbers: {autoNumber: "all"} } });
    </script>


