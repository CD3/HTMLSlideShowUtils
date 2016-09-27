#! /usr/bin/python
'''Configuration data functions.'''

# standard modules
import sys, os

# non-standard modules
import yaml
import dpath.util

def get_config_param( param, default, slidesfn ):

  config = dict()


  # look for user level config
  cfn = os.path.join( os.path.expanduser('~'), '.HTMLSlideShowUtils', 'config.yaml' )
  if os.path.isfile( cfn ):
    with open(cfn,'r') as f:
      dpath.util.merge( config, yaml.load(f) )

  # look for folder level config
  cfn = os.path.normpath( os.path.join( os.path.dirname(sys.argv[0] ), '..', 'config.yaml' ) )
  if os.path.isfile( cfn ):
    with open(cfn,'r') as f:
      dpath.util.merge( config, yaml.load(f) )

  # look for folder level config
  cfn = 'config.yaml'
  if os.path.isfile( cfn ):
    with open(cfn,'r') as f:
      dpath.util.merge( config, yaml.load(f) )


  # now get config in slides files
  text = ""
  if os.path.isfile( slidesfn ):
    with open(slidesfn,'r') as f:
      text = f.read()
  
  config_lines = list()
  config_lines.append("_trash : null")
  in_config = False
  for line in text.split('\n'):
    if in_config and line.strip() == '---':
      break

    if line.strip() == '---':
      in_config = True
      continue

    if in_config:
      config_lines.append(line)

  dpath.util.merge( config, yaml.load( "\n".join(config_lines) ) )

  try:
    return dpath.util.get( config, param )
  except:
    return default
