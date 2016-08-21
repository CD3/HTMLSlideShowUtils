---
push:
  user : username
  host : hostname
  root : public_html
  dest : slides/HTMLpresentations-demo

title  : HTML Presentations
subtitle : demo
---

# Math

LaTeX math is rendered using MathJax

$\nabla \cdot \vec{E} = \frac{\rho}{\epsilon_0}$

$\nabla \cdot \vec{B} = 0$

$\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}$

$\nabla \times \vec{B} = \mu_0\left( \vec{J} + \epsilon_0\frac{\partial \vec{E}}{\partial t}\right)$

The `\mathimg` macro will create an image of some LaTeX code (using
[tex2im](https://github.com/CD3/tex2im)) and include it instead. 
For example:![](eq-1.png). This doesn't
look as good as MathJax for inline math, but it allows you to use arbitrary LaTeX packages.

For example, this

\\mathimg{g = \\SI{9.8}{\\meter\\per\\second\\squared}}

will produce this

![](eq-2.png)

Since MathJax does not support the `siunitx`, this is the only way to use the \SI command.
You can also make the image larger, which is not possible with MathJax.

For example, this

\\mathimg[size="700x300"]{\\Delta E = \\delta Q + \\delta W}

will produce this

![](eq-3_700x300.png)


# Shell

The `shell` macro will run a command and include its output.

```
> ls
eq-1.png
eq-2.png
eq-3_500x500.png
eq-3_700x500.png
eq-3.png
Makefile
postprocessor
preprocessor
slides.md
slides-processed.md

```

