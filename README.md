# HTML Slide Show Utilities

A collection of utilities for creating HTML slide shows from markdown using `pandoc`.

## Description

`pandoc` can creating HTML slide shows from simple mardown files. This projects provides
a `Makefile` and some simple scripts to make this easy and add some useful features. For
example, the `Makefile` supports pushing an HTML slide show to a remote server. To build
and push a slide show, just run `make all`

The scripts also handle differences between the various slide show frameworks that pandoc
can write to so that you can create slide shows in each format from the same Markdown without
modification. Most of these differences have to deal with the css and javascript links. Some
of the output formats reference remote links (slidy) while others expect a specific
directory structure with the needed files to be present (revealjs, slideous).

## Usage

To get started, create a directory for your presentations, run the `setup.sh` in this directory,
and build the demo.

    > mkdir presentations
    > cd presentations
    > /path/to/this/dir/setup.sh
    > cd demo
    > make
    > firefox html/00-slides.html

This will build the example demo presentation.

To create your own presentation, you just need to create a new directory and link to the `Makefile`. Then
write you slides in a file named `slides.md`


    > mkdir myPres
    > cd myPres
    > ln -s ../Makefile ./
    > # create slides.md
    > make

Or use the `new-show` target
    > make new-show NAME=myPres
    > cd myPres
    > make

### Note
The `Makefile` is compatible with [`live-edit`](https://github.com/CD3/live-edit). To
automatically build and push your presentation on writes, edit the slides file with `live-edit`

    > live-edit slides.md  # make update is called each time slides.md is saved.
