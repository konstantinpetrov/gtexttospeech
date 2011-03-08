#!/usr/bin/env python

"""
Created by Paul Bagwell on 2011-03-08.
Copyright (c) 2011 Paul Bagwell. All rights reserved.

This module is used when gtexttospeech is run
as a standalone application.
"""

import sys
from .gtexttospeech import *
from optparse import OptionParser


def main():
    usage = 'Usage: %prog [options] arg1 arg2'
    parser = OptionParser(prog='gtexttospeech', usage=usage,
                          version='%prog 0.1')
    parser.add_option('-f', '--file', dest='filename', type='str', default='',
                      help='file, that contains phrases')
    parser.add_option('-o', '--outfile', dest='outfile', default='',
                      help='output mp3 file')
    parser.add_option('-t', '--text', dest='text',
                      help='phrase')
    parser.add_option('-l', '--language', dest='language',
                      help='phrase language (ru etc.)', default='ru')
    parser.add_option('-v', '--verbose',
                      action='store_true', dest='verbose', default=False,
                      help='be verbose')
    (options, args) = parser.parse_args()
    #print options.text
    if options.filename or options.text:
        kw = {'language': options.language}
        if options.filename:
            kw['text_or_file'] = open(options.filename)
            TextToSpeech(**kw).create(options.outfile)
        elif options.text:
            kw['text_or_file'] = options.text.decode('utf-8')
            TextToSpeech(**kw).create(options.outfile)
    elif len(args) >= 1:
        out = sys.stdout
        if len(args) >= 2:
            out = args[1]
        TextToSpeech(args[0].decode('utf-8')).create(out)
    else:
        s = sys.stdin.read().decode('utf-8')
        if not s:
            parser.print_help()
        else:
            TextToSpeech(s).create(sys.stdout)
    return 0

if __name__ == "__main__":
    sys.exit(main())
