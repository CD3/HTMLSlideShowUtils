#! /usr/bin/python
'''Get configuration parameters.'''

# standard modules
import re, argparse, importlib, os



missing_modules = list()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Check modules in python files.')
  parser.add_argument('file', nargs='+', help="Files to be checked.")

  args = parser.parse_args()

  local_modules = [ os.path.splitext( fn )[0] for fn in args.file ]

  for fn in args.file:
    with open(fn,'r') as f:
      text = f.read()

    for line in text.split('\n'):
      regex = re.compile('^\s*import\s+')
      if re.match( regex, line ):
        modules = [ mods.strip().split(' ')[0] for mods in re.sub( regex, '', line ).split(',') ]

        for module in modules:
          try:
            importlib.import_module(module)
          except:
            missing_modules.append( module )


  for module in missing_modules:
    print module
  
  
