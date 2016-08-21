To get started, create a new directory for your presentation and symlink to the
`Makefile`. Then write your presentation in a file name `slides.md` and run
`make`.

If you have a remote web server that you want to push to, configure the host
settings in the YAML metadata section.

    ---
    push:
      user: username
      host: hostname
      root: public_html
      dest: path/to/dest

    ... rest of configuration settings
    ---


The 'root' and 'dest' setting will be concatenated. This is useful if your webserver serves
out of some directory, such as public_html. You can set the root directory one, and then
just change the dest directory for each presentation.
