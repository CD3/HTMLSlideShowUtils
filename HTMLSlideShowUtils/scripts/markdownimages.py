#! /usr/bin/env python
'''Parses markdown file for images with size specification in the filename and creates them.'''

# standard modules
import sys, os, re, subprocess

# non-standard modules
from pyparsing import *

def get_image_filenames( text ):
  imagemarkdown = Suppress( Literal('!')+QuotedString(quoteChar='[', endQuoteChar=']') )+QuotedString(quoteChar='(', endQuoteChar=')')
  fns = list()
  for tokens in imagemarkdown.searchString( text ):
    fns.append(tokens[0])

  return fns
