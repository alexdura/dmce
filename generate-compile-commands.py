#!/usr/bin/env python

# Copyright (c) 2016 Ericsson AB
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys
import re
import os

lineindex = 0

# If there is a individual command file, read it. Otherwise revert to default command lines defined below
individualcmd=1
try:
    f = open(sys.argv[2], 'rb')
    lookupfile = f.readlines()
except IOError:
    individualcmd=0
    lookupfile = []

#default cmd line c
defaultcmdline_c = os.environ.get('DMCE_DEFAULT_C_COMMAND_LINE')

#default cmd line cpp
defaultcmdline_c = os.environ.get('DMCE_DEFAULT_C_COMMAND_LINE')

# Read from stdin
linebuf = sys.stdin.readlines()

# Construct list of file lines
linestotal = len(linebuf)
path = sys.argv[1] + "/"

# Retrieve individual command line
def IndividualCmdLine( sourcefile ):
   cmdline=""

# For now, special treatment for all regexp special characters. How is this done properly?!
   sourcefile = re.sub("\/", "\/", sourcefile)
   sourcefile = re.sub("\.", "\.", sourcefile)
   sourcefile = re.sub("\-", "\-", sourcefile)
   sourcefile = re.sub("\+", "\+", sourcefile)
   exp = sourcefile + "\s(.*)$"
   for file in lookupfile:
      found = re.match( exp, file, re.M|re.I)
      if (found):
          cmdline=found.group(1)
          break
   return cmdline

print "["

directory = ""
command = ""
filename = ""

while (lineindex<linestotal):
      directory = path
      filename = linebuf[lineindex].strip()
      command = IndividualCmdLine(filename)
      if (command == ""):
          m_c = re.match( r'.*\.c$', linebuf[lineindex], re.M|re.I)
          m_cc = re.match( r'.*\.cc$', linebuf[lineindex], re.M|re.I)
          m_cpp = re.match( r'.*\.cpp$', linebuf[lineindex], re.M|re.I)

          if (m_c):
              command = defaultcmdline_c + " " + filename
          elif (m_cc or m_cpp):
              command = defaultcmdline_cpp + " " + filename
          else:
              print "file cache corrupt!"
              exit(-1)

      print "{"
      print "\"directory\": \"" + directory + "\","
      print "\"command\": \"" + command + "\","
      print "\"file\": \"" + filename + "\""
      print "},"

      lineindex+=1

print "]"
