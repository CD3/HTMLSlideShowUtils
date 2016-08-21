# HTML Presentation Utilities

A collection of utilities for creating HTML slide shows from markdown using `pandoc`.

## Description

`pandoc` can creating HTML slide shows from simple mardown files. This projects provides
a `Makefile` and some simple scripts to make this easy and add some useful features. For
example, the `Makefile` supports pushing an HTML slide show to a remote server. To build
and push a slide show, just run `make all`

## Usage

To get started, create a directory for your presentations and run the `setup.sh` from
inside. The `setup.sh` script will copy the utilities into the directory.

    > mkdir presentations
    > cd presentations
    > /path/to/this/dir/setup.sh
    > mkdir presentation-1
    > cd presentation-1
    > ln -s ../Makefile
    > cp ../slides.md ./
    > make
    > firefox html/00-slides.html

This will build the example demo presentation.

The `Makefile` is compatible with [`live-edit`](https://github.com/CD3/live-edit). To
automatically build and push your presentation on writes, edit the slides file with `live-edit`

    > live-edit slides.md  # make update is called each time slides.md is saved.
