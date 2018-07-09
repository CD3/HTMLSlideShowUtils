#! /usr/bin/env python3

import os
import sys
import subprocess
import re
import pyparsing as pp
import collections

from argparse import ArgumentParser

parser = ArgumentParser(
    description="A tool for generating code demonstrations..")


parser.add_argument("-s", "--source",
                    action="store",
                    nargs="*",
                    default=[],
                    help="Source files to search for code in.",)

parser.add_argument("-e", "--executable",
                    action="store",
                    nargs="*",
                    default=[],
                    help="Executable files to run for output.",)

parser.add_argument("-n", "--demo-name",
                    action="store",
                    nargs="*",
                    default=[],
                    help="Demo section names to ouptut.",)

parser.add_argument("-l","--language",
                    action="store",
                    default="",
                    help="The language used in the source. This will be added to the code block that is generated to support syntax highlighting..",)

parser.add_argument( "--list-section-names",
                    action="store_true",
                    help="List the section names that were found.",)



args = parser.parse_args()

class Demo:
  def __init__(self):
    # self.data = collections.OrderedDict()
    self.data = dict()
    self.idx = 0
    self.UnnamedPrefix = "Unnamed-"

  def add(self,name,type,line):
    if name == "" or name is None:
      name = self.UnnamedPrefix+str(self.idx)
      self.idx += 1

    if name not in self.data:
      self.data[name] = dict()

    if type not in self.data[name]:
      self.data[name][type] = list()

    self.data[name][type].append(line)

  def add_source(self,name,source):
    self.add(name,'source',source)
  def add_output(self,name,output):
    self.add(name,'output',output)

  def names(self):
    return [ k for k in self.data.keys() if not k.startswith(self.UnnamedPrefix) ]


  class parser:
    beg = "#>"
    end = "#<"

    begin = pp.Literal(beg) + pp.OneOrMore(pp.Word(pp.alphanums))("name")
    end = pp.Literal(end)

        


  def parse( self, lines, type ):

    depth = 0
    name = ""
    for line in lines:
      line = line.strip('\n')
      result = Demo.parser.begin.searchString(line)
      if len(result):
        depth += 1
        name = ('|'.join(name.split('|') + [' '.join(result[0].name)])).strip('|')
        continue

      result = Demo.parser.end.searchString(line)
      if len(result):
        depth -= 1
        name = '|'.join(name.split('|')[0:-1])
        continue

      self.add(name,type,line)



  def write( self, stream, name = None ):


    matching_names = [ k for k in filter( re.compile(name, re.I).match, self.data.keys() ) ]

    lines = list()

    if len(matching_names) > 0:

      source = list()
      for name in matching_names:
        if 'source' in self.data[name]:
          source += self.data[name]['source']

      output = list()
      for name in matching_names:
        if 'output' in self.data[name]:
          output += self.data[name]['output']

      if len(source) > 0:
        lines.append("Code:")
        lines.append("```{0}".format(args.language))
        lines += source
        lines.append("```")
      
      if len(output) > 0:
        lines.append("\nOutput:")
        lines.append("```")
        lines += output
        lines.append("```")

    stream.write("\n".join(lines))






demo = Demo()

for file in args.source:
  with open(file,'r') as f:
    demo.parse(f,'source')

for exe in args.executable:
  result = subprocess.run(exe,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  demo.parse( result.stdout.decode('utf-8').split("\n"), 'output' )

names = args.demo_name
if len(names) == 1 and names[0].lower() == "all":
  names = ['.*']

if args.list_section_names:
  for name in demo.names():
    print("'{0}'".format(name))
  sys.exit(0)

for name in names:
  demo.write( sys.stdout, name )
