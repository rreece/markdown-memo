Mathematical expressions
===============================================================================

Spam
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
    \nabla \times \vec{E} &= \vec{j} + \frac{\partial \vec{E}}{\partial t} \nonumber \,.
\end{align}

Note that we are using [MathJax](https://www.mathjax.org/) to render
the equations in html. Our html template includes the following code
to ask MathJax to render it and number the equations:

    <!--- MathJax stuff -->
    <script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({ TeX: { equationNumbers: {autoNumber: "all"} } });
    </script>

Eggs
-------------------------------------------------------------------------------

Ei oratio mediocritatem sea, at choro mandamus disputando quo, id eius
albucius deseruisse mei. Id eam verear disputando repudiandae. Per et
clita reformidans. Ea his corpora ancillae fabellas, an eum facer tation
populo. Vix omittam lucilius inciderint ne, est cu civibus scribentur
adversarium.

