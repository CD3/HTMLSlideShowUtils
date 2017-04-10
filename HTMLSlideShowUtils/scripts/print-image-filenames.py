#! /usr/bin/python
'''Parses markdown file for images with size specification in the filename and creates them.'''

# standard modules
import sys, os, re, subprocess

# non-standard modules
from pyparsing import *

# local modules
import markdownimages

for fn in sys.argv[1:]:

  with open(fn,'r') as f:
    text = f.read()

  images = markdownimages.get_image_filenames(text)


  for fn in images:
    if not fn.startswith('http'):
      print fn
