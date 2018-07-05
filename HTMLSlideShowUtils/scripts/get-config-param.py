#! /usr/bin/env python2
'''Get configuration parameters.'''

# standard modules
import sys, os, argparse

# non-standard modules
import yaml
import dpath.util

# local modules
import config



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Retrieve configuration options.')
  parser.add_argument('param', help="Parameter (option) name to return.")
  parser.add_argument('--default'    , default=None         , help="Default value to return if parameter is not found.")
  parser.add_argument('--slides-file', default='slides.md'  , help="Slides file to query for configuration options.")
  parser.add_argument('--config-file', default='config.yaml', help="YAML configuration file to query for configuration options.")

  args = parser.parse_args()

  val = config.get_config_param( args.param, args.default, args.slides_file, args.config_file )
  print(val)
