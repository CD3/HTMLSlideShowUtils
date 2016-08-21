#! /usr/bin/python
'''Get configuration parameters.'''

# standard modules
import re, argparse, importlib



missing_modules = list()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Processes macros in text.')
  parser.add_argument('file', nargs='+', help="Files to be checked.")

  args = parser.parse_args()

  for fn in args.file:
    with open(fn,'r') as f:
      text = f.read()

    for line in text.split('\n'):
      regex = re.compile('^\s*import\s+')
      if re.match( regex, line ):
        modules = re.sub( regex, '', line ).replace(' ','').split(',')

        for module in modules:
          try:
            importlib.import_module(module)
          except:
            missing_modules.append( module )


  for module in missing_modules:
    print module
  
  
