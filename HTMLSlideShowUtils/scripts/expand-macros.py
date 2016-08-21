#! /usr/bin/python
'''Preprocess a markdown file by doing macro expansion an other things.'''

# standard modules
import sys, os, re, subprocess, argparse, tempfile

# non-standard modules
from pyparsing import *
from wand.image import Image
from wand.display import display

try:
  # support for user defined macro handlers
  import macros
  have_user_macros = True
except:
  have_user_macros = False


class MacroProcessor(object):

  def __init__(self):
    # macro grammer
    command = Word(alphas)
    options = originalTextFor( nestedExpr( '[', ']' ) )
    arguments = originalTextFor( nestedExpr( '{', '}' ) )

    self.macro = Combine( WordStart("\\") + Literal("\\") + command("command") + ZeroOrMore(options)("options") + ZeroOrMore(arguments)("arguments") )
    self.macro.setParseAction( self.expand )

  def process(self,text,repeat=True):

    while True:
      newtext = self.macro.transformString( text )

      if newtext == text or repeat == False:
        break
      text = newtext

    return text

  def expand(self,toks):

    command   = str(toks.command)
    # options and arguments are nested expressions. the token we get
    # will be wrapped in [] (for options) and {} (for arguments), so we need
    # to strip them off.
    options   = [ oo.strip() for o in toks.options for oo in str(o)[1:-1].split(',') ]
    arguments = [str(x)[1:-1] for x in toks.arguments]


    replacement = None
    if have_user_macros and hasattr(macros,command):
        replacement = getattr(macros,command)(self,arguments,options)
    elif hasattr(self,"command_"+command):
        replacement = getattr(self,"command_"+command)(arguments,options)


    return replacement

  def command_mathimg(self,args,opts):
    if len(args) < 1: # don't do anything if no argument was given
      return None

    # create an image file of the equation using our tex2im
    if not hasattr(self,'mathimg_num'):
      self.mathimg_num = 0
    self.mathimg_num += 1

    fn = "eq-%d.png"%(self.mathimg_num)
    cmd = "tex2im -o %s '%s' "%(fn,args[0])
    print "creating image of equation with:'"+cmd+"'"
    subprocess.call(cmd,shell=True)


    size=None
    if len(opts) > 0:
      oo = [ o.strip() for o in opts[0].split(',')]
      for o in oo:
        k,v = o.split('=')
        k = k.strip()
        v = v.strip()
        if k == 'size':
          size = v.strip('"')
          

    if size:
      fn = "eq-%d_%s.png"%(self.mathimg_num,size)

    # now replace the macro with markdown that points at the image
    md = '![](%s)'%fn

    return md




  def command_shell(self,args,opts):
    '''Run shell command and return output.'''
    with tempfile.TemporaryFile() as fp:
      cmd = ';'.join(args)
      subprocess.call( cmd, shell=True, stdout=fp )
      fp.seek(0)
      stdout = fp.read()

    return stdout


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Processes macros in text.')
  parser.add_argument('input_file', help="Files to be processed.")
  parser.add_argument('output_file', help="Name of file to write.")
  parser.add_argument('--debug', '-d', action='store_true', help="Output debug information.")

  args = parser.parse_args()

  with open(args.input_file,'r') as f:
    text = f.read()

  proc = MacroProcessor()
  text = proc.process(text)


  with open(args.output_file,'w') as f:
    f.write( text )
