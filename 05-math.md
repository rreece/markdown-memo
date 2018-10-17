Mathematical expressions
===============================================================================

<!-- PAGETOC -->

Typesetting math
-------------------------------------------------------------------------------

You can do latex inline like this:

    Euler's formula is remarkable: $e^{i\pi} + 1 = 0$.

Euler's formula is remarkable: $e^{i\pi} + 1 = 0$.

You can use `$$` to make an equation block like this:

    $$ \frac{\partial \rho}{\partial t} + \nabla \cdot \vec{j} = 0 \,. \label{eq:continuity} $$

$$ \frac{\partial \rho}{\partial t} + \nabla \cdot \vec{j} = 0 \,. \label{eq:continuity} $$

The latex equation environment can be used directly.
Stokes' theorem is pretty cool:

    \begin{equation} \label{eq:stokes}
        \int_{\partial\Omega} \omega = \int_{\Omega} \mathrm{d}\omega \,.
    \end{equation}

\begin{equation} \label{eq:stokes}
    \int_{\partial\Omega} \omega = \int_{\Omega} \mathrm{d}\omega \,.
\end{equation}

You can also refer to labeled equations, such as [@eq:stokes],
with the syntax:

    ... such as [@eq:stokes],

The `align` environment can also be used.
Maxwell's equations, [@eq:maxwell], are also tough to beat:

    \begin{align}
        \nabla \cdot  \vec{E} &= \rho \nonumber \\
        \nabla \cdot  \vec{B} &= 0    \nonumber \\
        \nabla \times \vec{E} &= - \frac{\partial \vec{B}}{\partial t} \label{eq:maxwell} \\
        \nabla \times \vec{B} &= \vec{j} + \frac{\partial \vec{E}}{\partial t} \nonumber \,.
    \end{align}

\begin{align}
    \nabla \cdot  \vec{E} &= \rho \nonumber \\
    \nabla \cdot  \vec{B} &= 0    \nonumber \\
    \nabla \times \vec{E} &= - \frac{\partial \vec{B}}{\partial t} \label{eq:maxwell} \\
    \nabla \times \vec{B} &= \vec{j} + \frac{\partial \vec{E}}{\partial t} \nonumber \,.
\end{align}


Mathjax
-------------------------------------------------------------------------------

When doing md $\rightarrow$ tex $\rightarrow$ pdf, LaTeX takes care of the math,
but to render the math in html, we use [MathJax](https://www.mathjax.org/).
Our html template includes the following code
to ask MathJax to render it and number the equations:

    $if(mathjax)$
    <!--- MathJax stuff -->
    <script type="text/javascript" src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({ TeX: { equationNumbers: {autoNumber: "all"} } });
    </script>
    $endif$


