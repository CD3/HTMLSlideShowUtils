#! /usr/bin/python
'''Get configuration parameters.'''

# standard modules
import sys, os, argparse

# non-standard modules
import yaml
import dpath.util

# local modules
import config



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Processes macros in text.')
  parser.add_argument('param', help="Parameter name to return.")
  parser.add_argument('--default', default=None, help="Default value.")
  parser.add_argument('--file', default='slides.md', help="Slides file.")

  args = parser.parse_args()

  val = config.get_config_param( args.param, args.default, args.file )
  print val
