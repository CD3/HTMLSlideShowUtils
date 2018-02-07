#! /usr/bin/env python

import subprocess, sys
from argparse import ArgumentParser

engines = { 'pandoc' : ['slidy', 'dzslides', 'reveal.js','slideous']
          , 'hovercraft' : ['impress.js']
          }

outputs = dict()
for e in engines:
  for o in engines[e]:
    if not o in outputs:
      outputs[o] = list()
    outputs[o].append(e)

if __name__ == "__main__":

  parser = ArgumentParser(description="Build slideshow from input file.")

  parser.add_argument("input_file",
                      action="store",
                      help="Input file to be processed." )

  parser.add_argument("output_file",
                      action="store",
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
                      default="markdown",
                      help="Input format." )


  args = parser.parse_args()

  
  if args.engine:
    engine = args.engine
  else:
    if args.to_format in outputs:
      engine = outputs[args.to_format][0]
    else:
      print("ERROR: could not find engine to support '%s' output."%args.to_format)
      sys.exit(1)

  if not engine in engines:
      print("ERROR: Unknown engine '%s'."%engine)
      sys.exit(1)

  if not args.to_format in outputs:
      print("ERROR: Unknown output format '%s'."%args.to_format)
      sys.exit(1)


  

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

  print "build cmd:",cmd
  print subprocess.check_output(cmd,shell=True)




