# HTML Slide Show Utilities

A collection of utilities for creating HTML slide shows from markdown using Pandoc.

## Description

`HTMLSlideShowUtils` is a collection of scripts that help automate the building
and deployment of HTML slides from a Markdown file.  It provides a `Makefile`
and some simple scripts to make this easy and add some useful features.  For
example, the `Makefile` supports pushing an HTML slide show to a remote server.
To build and push a slide show, just run `make all` All of the tools needed to
do this exist, this project simply provides some scripts to help streamline the
process.  Slide shows are build using `pandoc`, which support several
different HTML slide show frameworks.

The scripts also handle differences between the various slide show frameworks that `pandoc`
can write to so that you can create slide shows in each format from the same Markdown without
modification. Most of these differences have to deal with the CSS and javascript links. Some
of the output formats reference remote links (slidy) while others expect a specific
directory structure with the needed files to be present (revealjs, slideous).

## Installing

`HTMLSlideShowUtils` does not require installation. When you run the setup script (see below)
a local copy of the utilities directory is created so that this directory could be copied
to another directory or computer and still run. However, the utility scripts require
Pandoc and a few python modules to be installed. When the setup script runs (see below),
it will try to detect any missing dependencies and tell you what needs to be installed.

## Usage

To get started, create a directory for your presentations, run the `setup.sh` script in this directory,
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

To update the utilities, simply run the `setup.sh` script in the presentations directory. This will automatically
rerun the `setup.sh` script in the `HTMLSlideShowUtils` repo.

    > cd presentations
    > ./setup.sh

### Note

The `Makefile` is compatible with [`live-edit`](https://github.com/CD3/live-edit). To
automatically build and push your presentation on writes, edit the slides file with `live-edit`

    > live-edit slides.md  # make update is called each time slides.md is saved.

### Macros

Macros provide a mechanism to extend Markup un-intrusively. The `Makefile` that builds the slide show first creates a copy of `slides.md` named `slides-processed.md` and
then runs a series of commands that may modify this file. The modified file is then compiled by `pandoc` into an HTML slide show. This allows for some preprocessing to occur
before `pandoc` is run. One of the preprocessing steps that will be performed is macro expansion.

Macros follow the LaTeX command syntax: `\commandname[options]{arguments}`. The `expand-macros.py` script will read `slides-processed.md` and attempt to expand any macros that it
finds. Unrecognized macros are left in place. The script provides several useful macros.

`\mathimg{latex snippet}`
: Create an image file (png) from a LaTeX snippet and include the image in the slide. This macro uses [`tex2im`](https://github.com/CD3/tex2im) to create a png of the LaTeX snippet.
  Use of arbitrary LaTeX packages are supported, but must `tex2im` must be configured to include them.

`\scriptimg{script text}`
: Run a script to create an image file (png) and include the image into the slide. The script text should include the shebang and the script should create a file named `out.png` which will be renamed after the script is ran.
  This macro writes the script to a text file, makes the file executable, runs the file, and then moves `out.png` to a unique filename that is included into the slide.

`\image{image url}`
: This macro is similar to the markdown \!\[\](imagename) command, except that it accepts remote image urls. The image will be downloaded and included in the slide.

`\shell{shell command}`
: Run a shell command and include its output. This macro lets you insert the output of a shell command into the slide, which is useful for presentations on command line applications.


In addition to these, user defined macros can be created. In order to create a new macro, or overload an existing macro, you just need to write python functions that will perform the macro
expansion in a file named `macros.py`. If this file exits, `expand-macros.py` will load all of the functions defined in it and use them to expand macros. The function signature should be

```
 def macroname(self, args, opts):
   ...

   return str
```

The function should return a string that will replace the macro.  The instance
of the macro expansion class that is performing the macro expansion is passed
into the first argument `self`. This gives you access to the members of the
class, but is currently undocumented.  However, you can use `self` to save
state information between macro calls, for example to keep track of how many
times the macro was expanded. The second argument that contains the string
found in square brackets and the third argument will be a list of the strings
found in curly brackets (multiple curly brackets are possible, just as with
LaTeX).  The function that performs the macro expansion is responsible for
parsing all options and arguments, so the example given could be implemented as
`\macroname[option1="true",option2="true"]{argument}`, but the function that
does the expansion would be responsible for parsing the ',' into two separate
options.


## FAQ

### Why is this better than PowerPoint?

Honestly, for most people it isn't.  Before this, I was using PowerPoint, and
do not really have a problem with anything PowerPoint does in terms of creating
and giving a presentation.  It is even possible to get true LaTeX support with
the IguanaTex add-in, and I certainly like it better than the
OpenOffice/LiebreOffice presentation software.

This project grew out of a frustration with editing presentations. Specifically the fact that *all* editing must
go through the PowerPoint interface. So, if I want to make a change to a presentation, I have to have a copy of
PowerPoint on my computer, I have to open it up, and I have to click around. Then, if I want to make my presentation
available to others without requiring PowerPoint (to students for example), I have to do some more clicking to
export the slides to PDF. Any time I make a change, I have to do this.

So I wanted something that was more flexible, and could be automated. I started looking around, and after about
a year of testing out different solutions, I ended up here.

### Why is this better than [madoko](https://www.madoko.net/)

Madoko is actually the first tool I used to create HTML slides, and it works pretty well. It is defiantly better
than PowerPoint in terms of flexibility. You write your presentation in plain text using Markdown and Madoko
turns it into an HTML file that you can then view in any web browser. Using Markdown is great because it is simple
and easy to read. So Madoko does all the hard work of getting this turned into a javascript driven slide show.

In the end, there were a few quirks that are probably more reveal.js than madoko that caused me to look for alternatives.
Once I tried Pandoc, I found that it could basically do everything I liked about madoko and more.

