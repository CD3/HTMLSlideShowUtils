#! /usr/bin/python
'''Configuration data functions.'''

# standard modules

# non-standard modules
from pyparsing import *

def parse_options_str( opts_str ):
  '''Parse a string of comma separated options and return a dict.'''

  if isinstance( opts_str, list ):
    return [ parse_options_str(o) for o in opts_str ]


  key = Word(alphas, alphanums+'_')
  val = QuotedString(quoteChar='"')
  opt = key("key") + "=" + val("val")


  options = dict()
  for o in opt.searchString( opts_str ):
    options[o['key']] = o['val']

  return options


