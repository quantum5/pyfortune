from __future__ import unicode_literals
import os
import random

class FortuneFile(object):
    def __init__(self, file, path=None):
        self.file = file
        self.path = path if path is not None else getattr(file, 'name', None)
        self.__parse_fortune()
    
    def __parse_fortune(self):
        self.fortunes = fortunes = []
        buf = []
        for line in self.file:
            line = line.rstrip('\r\n')
            if line == '%':
                fortunes.append('\n'.join(buf))
                buf = []
            else:
                buf.append(line)
        if buf:
            fortunes.append('\n'.join(buf))
        self.size = len(fortunes)
        self.file.close()
    
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
    
    def __unicode__(self):
        if self.path is not None:
            return '<Fortune File: Path: %s>' % self.path
        return '<Fortune File: %s>' % self.file
    
    def __str__(self):
        return unicode(self).encode('mbcs' if os.name == 'nt' else 'utf-8', 'xmlcharrefescape')
