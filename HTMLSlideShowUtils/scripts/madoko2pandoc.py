#! /usr/bin/env python

# standard modules
import sys, os, re

# non-standard modules
import pyparsing

for fn in sys.argv[1:]:

  with open(fn,'r') as f:
    lines = f.read().split('\n')

  has_header = False
  if re.search( re.compile('^\[title\]',re.M), '\n'.join(lines).lower() ):
    has_header = True
    lines.insert(0,'---')

  in_header = False
  if has_header:
    in_header = True

  for i in range(len(lines)):
    if re.search('{.fragment}', lines[i]):
      lines[i] = re.sub('{.fragment}', '', lines[i])
      lines[i] = re.sub('^', '\n> ', lines[i])

    if lines[i].replace(" ","").lower() == "[title]":
      lines[i] = '---'
      in_header = False

    if lines[i].replace(" ","").lower().startswith("[include"):
      lines[i] = ''

    if in_header:
      lines[i] = re.sub( "^Title", "title", lines[i] )


  bn,ext = os.path.splitext( fn )
  fn = bn+'-pandoc'+ext
  with open(fn, 'w') as f:
    f.write( '\n'.join(lines) )
