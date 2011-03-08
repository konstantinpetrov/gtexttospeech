#!/usr/bin/env python
# encoding: utf-8
"""
gtexttospeech.py

Created by Paul Bagwell on 2011-03-08.
Copyright (c) 2011 Paul Bagwell. All rights reserved.
"""

import os
import urllib2
import unittest
from codecs import open as uopen
from cookielib import CookieJar
from glob import glob
from math import ceil
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
from urllib import urlencode


__all__ = ['TextToSpeechError', 'TextToSpeech']


class TextToSpeechError(Exception):
    pass


class TextToSpeech(object):
    replacers = (  # list of replacers
        (u'ё', u'йо'),
        (u'трех', u'трьох'),
        (u'хабрахабр', u'хабрах+абр'),
    )

    def __init__(self, text_or_file, replacers=None, language='ru'):
        if isinstance(text_or_file, file):
            with uopen(text_or_file.name, encoding='utf-8') as f:
                text = f.read()
            text_or_file.close()  # close non-unicode file
        else:
            text = text_or_file
        self.sentences = self.split_by_len(text)
        self.language = language
        if replacers and isinstance(replacers, (list, tuple)):
            self.replacers = replacers
        self.tmp = []  # list of temporary downloaded mp3s
        self.updated_url_openers = False

    def update_url_openers(self):
        """Updates urlopeners with various required by google headers."""
        headers = (
            ('Host', 'translate.google.com'),
            ('User-Agent', ('Mozilla/5.0 (Windows; U; Windows NT 6.1;'
                ' en-US; rv:2.0.0) Gecko/20110320 Firefox/4.0.0')),
            ('Accept', 'text/html,application/xhtml+xml,'
                'application/xml;q=0.9,*/*;q=0.8'),
            ('Accept-Language', 'en-us,en;q=0.5'),
            ('Accept-Encoding', 'gzip,deflate'),
            ('Accept-Charset', 'utf-8;q=0.7,*;q=0.7'),
            ('Keep-Alive', '115'),
            ('Connection', 'keep-alive'),
        )

        jar = CookieJar()
        handler = urllib2.HTTPCookieProcessor(jar)
        opener = urllib2.build_opener(handler)
        opener.addheaders = headers
        urllib2.install_opener(opener)
        self.updated_url_openers = True

    def make_url(self, text):
        """Generates url to Google Translate MP3 file."""
        tpl = u'http://translate.google.com/translate_tts?q=[{0}]&tl={1}'
        return tpl.format(
            urlencode({'': text.encode('utf-8')}).strip('=').strip('\n'),
            self.language
        )

    def split_by_len(self, text, length=95):
        """Splits files by sentences with maximum length=length."""
        for r in self.replacers:
            text = text.replace(r[0], r[1])
        if len(text) < length:
            return [text]
        SEP = ' '
        sentences = []
        t = text.split(SEP)

        def make_list(x, y):
            args = [x, y]
            joined = SEP.join(args)
            for i in args:
                if len(i) > length:
                    t = u'Length of word {0} is too big'
                    raise TextToSpeechError(t.format(i))
            if len(joined) < length:
                return joined
            sentences.append(x)
            return y
        last_sentence = reduce(make_list, t)
        sentences.append(last_sentence)
        return sentences

    def download_voices(self, sentences):
        """Downloads MP3s."""
        if not self.updated_url_openers:
            self.update_url_openers()
        for line in sentences:
            mp3 = NamedTemporaryFile(suffix='.mp3', delete=False)
            url = self.make_url(line)
            content = urllib2.urlopen(url.encode('utf-8')).read()
            mp3.write(content)
            mp3.close()
            self.tmp.append(open(mp3.name, 'rb'))

    def delete_voices(self):
        """Deletes all downloaded files."""
        for f in self.tmp:
            f.close()
            os.unlink(f.name)
        self.tmp = []

    def join_voices(self, result_file):
        """Copies audiodata from all downloaded MP3s to result_file."""
        for f in self.tmp:
            copyfileobj(f, result_file)

    def create(self, result_file, delete_tmp_files=True):
        """Downloads all voices and copies them to result_file."""
        if not self.tmp:
            self.download_voices(self.sentences)
        if not isinstance(result_file, file):
            result_file = open(result_file, 'wb+')
        self.join_voices(result_file)
        if delete_tmp_files:
            self.delete_voices()
