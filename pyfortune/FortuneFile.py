from __future__ import unicode_literals
from pyfortune.compile import sthead, stentry
import os
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
        buf = []
        for line in self.file:
            line = line.rstrip(b'\r\n')
            if line == b'%':
                fortunes.append(b'\n'.join(buf).decode('utf-8', 'replace'))
                buf = []
            else:
                buf.append(line)
        if buf:
            fortunes.append(b'\n'.join(buf).decode('utf-8', 'replace'))
        self.size = len(fortunes)
    
    def choose(self, long=None, size=160, count=1):
        if long:
            fortunes = [fortune for fortune in self.fortunes if len(fortune) > size]
        elif long == False:
            fortunes = [fortune for fortune in self.fortunes if len(fortune) <= size]
        else:
            fortunes = self.fortunes
        if len(fortunes) < count:
            return None
        sample = random.sample(fortunes, count)
        return sample[0] if count == 1 else sample
    
    def compile(self, file):
        if self.mtime is None:
            return # Can't and won't compile
        data = self.file
        data.seek(0, 0)
        start = 0
        end = None
        file.write(sthead.pack(0xDEADFACE, len(self.fortunes), 0, self.mtime))
        while True:
            line = data.readline()
            if not line:
                break
            if line.rstrip(b'\r\n') == b'%':
                if end is not None:
                    file.write(stentry.pack(start, end - start))
                start = data.tell()
                end = None
            else:
                end = data.tell()
        if end is not None:
            file.write(stentry.pack(start, end - start))
    
    def __unicode__(self):
        if self.path is not None:
            return '<Fortune File: Path: %s>' % self.path
        return '<Fortune File: %s>' % self.file
    
    def __str__(self):
        return unicode(self).encode('mbcs' if os.name == 'nt' else 'utf-8', 'xmlcharrefescape')
