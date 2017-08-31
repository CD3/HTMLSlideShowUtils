#! /usr/bin/python
'''Prints a set of command line options to pass to pandoc for a given file.'''

# standard modules
import sys, os, argparse

# non-standard modules
import yaml
import dpath.util



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Processes macros in text.')
  parser.add_argument('to', help="The format to be written. Will be same as the --to argument to pandoc.")

  args = parser.parse_args()

  opts = list()


  
  if args.to == "slidy":
    # allow easy css overloads
    opts.append("--css %s_extra.css"%args.to)
    opts.append("--variable %s-url='./data'"%args.to)
    
  if args.to == "dzslides":
    opts.append("--css ./data/dzslides.css")
    opts.append("--css %s_extra.css"%args.to)

  if args.to == "revealjs":
    opts.append("--css %s_extra.css"%args.to)
    opts.append("--variable %s-url='./data'"%args.to)

  if args.to == "slideous":
    opts.append("--css %s_extra.css"%args.to)
    opts.append("--variable %s-url='./data'"%args.to)

  print(" ".join( opts ))

