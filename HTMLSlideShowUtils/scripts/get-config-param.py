#! /usr/bin/python
'''Get configuration parameters.'''

# standard modules
import sys, os, argparse

# non-standard modules
import yaml
import dpath.util



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Processes macros in text.')
  parser.add_argument('param', help="Parameter name to return.")
  parser.add_argument('--default', default=None, help="Default value.")
  parser.add_argument('--file', default='slides.md', help="Slides file.")

  args = parser.parse_args()

  text = ""
  if args.file:
    with open(args.file,'r') as f:
      text = f.read()
  

  config = dict()


  # look for user level config
  cfn = os.path.join( os.path.expanduser('~'), '.HTMLSlideShowUtils', 'config.yaml' )
  if os.path.isfile( cfn ):
    with open(cfn,'r') as f:
      config.update( yaml.load(f) )

  # look for folder level config
  cfn = os.path.normpath( os.path.join( os.path.dirname(sys.argv[0] ), '..', 'config.yaml' ) )
  if os.path.isfile( cfn ):
    with open(cfn,'r') as f:
      config.update( yaml.load(f) )


  # now get config in slides files
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

  config.update( yaml.load( "\n".join(config_lines) ) )


  try:
    print dpath.util.get( config, args.param )
  except:
    print "null"
