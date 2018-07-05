#! /usr/bin/env python2

import subprocess, sys, os
from argparse import ArgumentParser

engines = { 'pandoc' : {'in' : ['markdown', 'md'],
                        'out' : ['slidy', 'dzslides', 'reveal.js','slideous']}
          , 'hovercraft' : {'in' : ['restructuredtext', 'rst'],
                            'out' : ['impress.js'] }
          }

output_fmts = dict()
for e in engines:
  for o in engines[e]['out']:
    if not o in output_fmts:
      output_fmts[o] = list()
    output_fmts[o].append(e)

input_fmts = dict()
for e in engines:
  for i in engines[e]['in']:
    if not i in input_fmts:
      input_fmts[i] = list()
    input_fmts[i].append(e)


if __name__ == "__main__":

  # parse options
  parser = ArgumentParser(description="Build slideshow from input file.")

  parser.add_argument("input_file",
                      action="store",
                      default="slides.md",
                      help="Input file to be processed." )

  parser.add_argument("output_file",
                      action="store",
                      default="00-slides.md",
                      help="Output file." )

  parser.add_argument("-e", "--engine",
                      action="store",
                      type=str,
                      help="Engine to build slideshow with." )

  parser.add_argument("-t", "--to-format",
                      action="store",
                      type=str,
                      default="slidy",
                      help="Output format." )

  parser.add_argument("-f", "--from-format",
                      action="store",
                      type=str,
                      help="Input format." )


  args = parser.parse_args()

  # detect input format if not given
  input_fmt = args.from_format
  if not input_fmt:
    trash,ext = os.path.splitext(args.input_file)
    input_fmt = ext[1:]

  # detect output format if not given
  if not input_fmt in input_fmts:
    print("ERROR: could not find engine to support '%s' input."%input_fmt)
    sys.exit(1)

  output_fmt = args.to_format
  if not output_fmt in output_fmts:
      print("ERROR: Unknown output format '%s'."%output_fmt)
      sys.exit(1)

  
  # find an engine
  engine = output_fmts[output_fmt][0]

  if engine == "pandoc":
    # pandoc options:
    # --self-contained does not work with mathjax
    # --standalone creates a file with header and footer
    # --mathjax uses mathjax javascript to render latex equation. requires an internet connection
    # --to is the format that will be written to
    cmd = "pandoc {INPUT} -o {OUTPUT} --standalone --mathjax --to {TO} "
    if args.to_format == "slidy" or args.to_format == "reveal.js" or args.to_format == "slideous":
      cmd += " --css {TO}_extra.css --variable {TO}-url='./data'"
    if args.to_format == "dzslides":
      cmd += " --css ./data/dzslides.css --css {TO}_extra.css"

    cmd = cmd.format(INPUT=args.input_file,OUTPUT=args.output_file,TO=args.to_format)

  if engine == "hovercraft":
    cmd = "hovercraft {INPUT} {OUTPUTDIR}"
    
    # cmd += " --css {TO}_extra.css"
    odir,ofn = os.path.split( args.output_file )
    if odir == "":
      odir = "."
    cmd = cmd.format(INPUT=args.input_file,OUTPUTDIR=odir,TO=args.to_format)

  print "build cmd:",cmd
  print subprocess.check_output(cmd,shell=True)




