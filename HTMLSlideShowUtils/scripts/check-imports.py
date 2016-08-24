#! /usr/bin/python
'''Get configuration parameters.'''

# standard modules
import re, argparse, importlib, os



missing_modules = list()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Check modules in python files.')
  parser.add_argument('file', nargs='+', help="Files to be checked.")

  args = parser.parse_args()

  local_modules = [ os.path.splitext( os.path.basename( fn ) )[0] for fn in args.file ]

  for fn in args.file:
    with open(fn,'r') as f:
      text = f.read()

    for line in text.split('\n'):
      modules = []

      # standard import style
      import_regex = re.compile('^\s*import\s+')
      if re.match( import_regex, line ):
        modules = [ mods.strip().split(' ')[0] for mods in re.sub( import_regex, '', line ).split(',') ]

      # from module import -style
      from_regex = re.compile('^\s*from\s+\S+\s+import')
      if re.match( from_regex, line ):
        modules = [ re.sub( '^\s*from\s+','', line ).split(' ')[0].strip() ]

      for module in modules:
        try:
          importlib.import_module(module)
        except:
          missing_modules.append( module )


  for module in missing_modules:
    if module not in local_modules:
      print module
  
  
