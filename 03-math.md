Mathematical expressions
===============================================================================

Typestting math
-------------------------------------------------------------------------------

You can do latex in-line, $e^{i\pi} + 1 = 0$.
You can also refer to labeled equations, such as eq.\ $\eqref{eq:stokes}$.

Stokes' theorem is pretty cool:

\begin{equation} \label{eq:stokes}
    \int_{\partial\Omega} \omega = \int_{\Omega} \mathrm{d}\omega \,.
\end{equation}

Maxwell's equations $\eqref{eq:maxwell}$ are also tough to beat:

\begin{align}
    \nabla \cdot  \vec{E} &= \rho \nonumber \\
    \nabla \cdot  \vec{B} &= 0    \nonumber \\
    \nabla \times \vec{E} &= - \frac{\partial \vec{B}}{\partial t} \label{eq:maxwell} \\
    \nabla \times \vec{B} &= \vec{j} + \frac{\partial \vec{E}}{\partial t} \nonumber \,.
\end{align}


Mathjax to render the math on the web
-------------------------------------------------------------------------------

When doing md &rarr; tex &rarr; pdf, LaTeX takes care of the math,
but to render the math in html, we use [MathJax](https://www.mathjax.org/).
Our html template includes the following code
to ask MathJax to render it and number the equations:

    <!--- MathJax stuff -->
    <script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({ TeX: { equationNumbers: {autoNumber: "all"} } });
    </script>



