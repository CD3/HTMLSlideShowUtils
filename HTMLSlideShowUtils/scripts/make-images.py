#! /usr/bin/env python
'''Parses markdown file for images with size specification in the filename and creates them.'''

# standard modules
import sys, os, re, subprocess, argparse

# non-standard modules
from pyparsing import *
from wand.image import Image
from wand.display import display

# local modules
import markdownimages

parser = argparse.ArgumentParser(description='Make resized images from graphics links in a markdown file.')
parser.add_argument('file', nargs='+', help="Files to be searched.")
parser.add_argument('--skip-existing', '-s', action='store_true', help="Skip files that that already exist.")

args = parser.parse_args()


for fn in args.file:

  with open(fn,'r') as f:
    text = f.read()

  images = markdownimages.get_image_filenames(text)

  size          = Word(nums+'W')("width") + 'x' + Word(nums+'H')("height")
  ext           = Combine('.' + Word(alphas))("ext")
  metadata      = '_'+size+ext

  for fn in images:
    meta = metadata.searchString( fn )
    if len(meta)>0:
      meta = meta[-1] # if there where multiple matches, we want the last one
      bn = fn.replace( ''.join(meta), '' )

      ifn = bn+meta.ext
      ofn = fn
      if args.skip_existing and os.path.isfile( ofn ):
        continue
      else:
        with Image(filename=ifn) as img:
          print("Creating",ofn,"from",ifn)
          with img.clone() as nimg:
            width  = long(meta.width) if meta.width != 'W' else meta.width
            height = long(meta.height) if meta.height != 'H' else meta.height

            if width == 'W' and height == 'H':
              width = nimg.width

            if width == 'W':
              width = long(nimg.width * float(height)/float(nimg.height))

            if height == 'H':
              height = long(nimg.height * float(width)/float(nimg.width))

            nimg.resize( width,height )


            nimg.save(filename=ofn)


