#! /usr/bin/python
'''Parses markdown file for images with size specification in the filename and creates them.'''

# standard modules
import sys, os, re, subprocess

# non-standard modules
from pyparsing import *
from wand.image import Image
from wand.display import display

# local modules
import markdownimages


for fn in sys.argv[1:]:

  with open(fn,'r') as f:
    text = f.read()

  images = markdownimages.get_image_filenames(text)

  size          = Combine(Word(nums) + 'x' + Word(nums))
  ext           = Combine('.' + Word(alphas))
  metadata      = '_'+size+ext

  for fn in images:
    meta = metadata.searchString( fn )
    if len(meta)>0:
      meta = meta[-1] # if there where multiple matches, we want the last one
      _,geom,ext = meta
      bn = fn.replace( ''.join(meta), '' )

      ifn = bn+ext
      ofn = fn

      with Image(filename=ifn) as img:
        print "Creating",ofn,"from",ifn
        with img.clone() as nimg:
          size = [ int(x) for x in geom.split('x') ]
          nimg.resize( *size )
          nimg.save(filename=ofn)


