#! /usr/bin/python
'''Preprocess a markdown file by doing macro expansion an other things.'''

# standard modules
import sys, os, re, subprocess, argparse, tempfile, urlparse, urllib

# non-standard modules
from pyparsing import *

# local modules
import options as op

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
    '''Create an image from LaTeX code and include it.'''

    if len(args) < 1: # don't do anything if no argument was given
      return None

    # create an image file of the equation using our tex2im
    if not hasattr(self,'mathimg_num'):
      self.mathimg_num = 0
    self.mathimg_num += 1

    extra_opts=""
    if len(opts) > 1:
      extra_opts = opts[1]


    ifn = "eq-%d.png"%(self.mathimg_num)
    ofn = "eq-%d.log"%(self.mathimg_num)
    cmd = "tex2im -o %s %s '%s' "%(ifn,extra_opts,args[0])
    print "creating image of equation with:'"+cmd+"'"
    with open(ofn,'w') as f:
      status = subprocess.call(cmd,shell=True,stdout=f,stderr=f)
      if status != 0:
        print "\tWARNING: there was a problem running tex2im."
        print "\tWARNING: command output was left in %s"%(ofn)
        print "\tWARNING: replacing with $...$, which may not work..."
        return "$"+args[0]+"$"


    options = op.parse_options_str( opts )

    size = None
    if len(options) > 0:
      if 'size' in options[0]:
        size = options[0]['size']
      else:
        size = '{width}x{height}'.format( width=options[0].get('width','W'), height=options[0].get('height','H') )
          
      if size:
        ifn = "eq-%d_%s.png"%(self.mathimg_num,size)

    # now replace the macro with markdown that points at the image
    md = '![](./%s)'%ifn

    return md

  def command_scriptimg(self,args,opts):
    '''Create an image from a script and include it.'''

    if len(args) < 1: # don't do anything if no argument was given
      return None

    # create an image file of the equation using our tex2im
    if not hasattr(self,'scriptimg_num'):
      self.scriptimg_num = 0
    self.scriptimg_num += 1

    extra_opts=""
    if len(opts) > 1:
      extra_opts = opts[1]


    sfn = "sc-%d.txt"%(self.scriptimg_num)
    ifn = "sc-%d.png"%(self.scriptimg_num)
    ofn = "sc-%d.log"%(self.scriptimg_num)

    with open(sfn,'w') as f:
      f.write(re.sub( "^\s*#","#",args[0] ) )

    cmd = "chmod +x %s; ./%s; mv out.png %s"%(sfn,sfn,ifn)
    print "creating image from script with:'"+cmd+"'"
    with open(ofn,'w') as f:
      status = subprocess.call(cmd,shell=True,stdout=f,stderr=f)
      if status != 0:
        print "\tWARNING: there was a problem running script."
        print "\tWARNING: the script and its output were left in %s and %s"%(sfn,ofn)
        return "ERROR: could not create image"


    options = op.parse_options_str( opts )

    size = None
    if len(options) > 0:
      if 'size' in options[0]:
        size = options[0]['size']
      else:
        size = '{width}x{height}'.format( width=options[0].get('width','W'), height=options[0].get('height','H') )
          
      if size:
        ifn = "sc-%d_%s.png"%(self.scriptimg_num,size)

    # now replace the macro with markdown that points at the image
    md = '![](./%s)'%ifn

    return md

  def command_image(self,args,opts):
    '''Insert a (possibly remote) image.'''
    fn = args[0]
    options = op.parse_options_str( opts )

    url = urlparse.urlparse(fn)
    if url.scheme == '':
      url = url._replace(scheme='file')

    if url.scheme == 'file':
      fn = os.path.join( os.getcwd(), fn)
      fn = os.path.normpath(fn)
      if not os.path.isfile( fn ):
        raise RuntimeError("ERROR: could not find image file '%s'." % fn )
      url = url._replace(path=fn)

    lfn = os.path.basename(url.path)
    url = url.geturl()

    # get size from options
    size = None
    if len(options) > 0:
      if 'size' in options[0]:
        size = options[0]['size']
      else:
        size = '{width}x{height}'.format( width=options[0].get('width','W'), height=options[0].get('height','H') )
          
      if size:
        n,e = os.path.splitext(lfn)
        lfn = "%s_%s%s"%(n,size,e)


    if fn != lfn:
      # download the image
      with open(lfn,'wb') as lf:
        f = urllib.urlopen(url)
        lf.write(f.read())
        f.close()

    return '![](./%s)'%lfn


  command_includegraphics = command_image


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
