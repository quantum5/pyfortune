from __future__ import unicode_literals
from pyfortune.compile import sthead, stentry
import os
import sys
import random

class FortuneFile(object):
    def __init__(self, file, path=None, mtime=None):
        self.file = file
        self.path = path if path is not None else getattr(file, 'name', None)
        try:
            self.mtime = int(os.path.getmtime(self.path)) if mtime is None else mtime
        except os.error:
            self.mtime = None
        self.__parse_fortune()
    
    def __parse_fortune(self):
        self.fortunes = fortunes = []
        self.table = table = []
        data = self.file
        buf = []
        start = 0
        merge = b''.join
        addfortune = fortunes.append
        addtable = table.append
        addbuf = buf.append
        tell = data.tell
        for line in data:
            if line[:1] == b'%':
                length = len(line)
                a = len(merge(buf))
                addfortune(merge(buf))
                del buf[:]
                end = tell()
                addtable((start, end - start - length))
                start = end
                continue
            addbuf(line)
        if buf:
            addfortune(b'\n'.join(buf))
            addtable((start, tell() - start))
        self.size = len(fortunes)
    
    def choose(self, long=None, size=160, count=1):
        if long:
            fortunes = [fortune for fortune in self.fortunes
                        if len(fortune) > size]
        elif long == False:
            fortunes = [fortune for fortune in self.fortunes
                        if len(fortune) <= size]
        else:
            fortunes = self.fortunes
        if len(fortunes) < count:
            return None
        sample = [i.rstrip('\r\n').decode('utf-8', 'replace')
                  for i in random.sample(fortunes, count)]
        return sample[0] if count == 1 else sample
    
    def compile(self, file):
        if self.mtime is None:
            return # Can't and won't compile
        file.write(sthead.pack(0xDEADFACE, len(self.fortunes), 0, self.mtime))
        file.write(b''.join(stentry.pack(start, length) for start, length in self.table))
    
    def __unicode__(self):
        if self.path is not None:
            return '<Fortune File: Path: %s>' % self.path
        return '<Fortune File: %s>' % self.file
    
    if int(sys.version[0]) > 2:
        __str__ = __unicode__
    else:
        def __str__(self):
            return unicode(self).encode('mbcs' if os.name == 'nt' else 'utf-8', 'xmlcharrefescape')
