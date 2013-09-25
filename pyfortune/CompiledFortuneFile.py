from pyfortune.FortuneFile import FortuneFile
from pyfortune.compile import sthead, stentry
import struct
import os
import io
import sys
import random

if int(sys.version[0]) > 2:
    xrange = range

class CompiledFortuneFile(FortuneFile):
    def __init__(self, path):
        self.compiled_path = path
        self.data_path = os.path.splitext(path)[0]
        self.data = None
        self.compiled = io.open(path, 'rb')
        self.mtime = int(os.path.getmtime(self.data_path))
        self.__load_compiled()
    
    @classmethod
    def stream(cls, compiled, data, compiled_path=None, data_path=None):
        self = cls.__new__(cls)
        self.compiled_path = compiled_path
        self.data_path = data_path
        self.data = data
        self.compiled = compiled
        self.mtime = 0
        self.__load_compiled()
        return self
    
    def __load_compiled(self):
        self.version, self.size, self.flags, mtime = sthead.unpack(self.compiled.read(sthead.size))
        if self.version != 0xDEADFACE:
            raise ValueError('Compiled file of the future!')
        if mtime < self.mtime:
            raise ValueError('Outdated compiled file')
    
    def __load_fortunes(self, entry=stentry.unpack, block=stentry.size):
        if not hasattr(self, 'fortunes'):
            read = self.compiled.read
            self.fortunes = []
            data = read()
            add = self.fortunes.append
            start = 0
            for i in xrange(self.size):
                buf = data[start:start+block]
                if len(buf) < block:
                    break
                add(entry(buf))
                start += block
            if len(self.fortunes) != self.size:
                logger.error('%s: Compiled file wrong length', self.compiled_path)
                if self.compiled_path:
                    try:
                        os.unlink(self.compiled_path)
                    except OSError:
                        # Dying here with a pretty message
                        raise SystemExit('Invalid Compiled File: %s' % self.compiled_path)
            self.compiled.close()
    
    def __open_data(self):
        if self.data is None:
            self.data = io.open(self.data_path, 'rb')
    
    def choose(self, long=None, size=160, count=1):
        self.__load_fortunes()
        if long:
            fortunes = [(o, l) for o, l in self.fortunes if l > size]
        elif long == False:
            fortunes = [(o, l) for o, l in self.fortunes if l <= size]
        else:
            fortunes = self.fortunes
        if len(fortunes) < count:
            return None
        sample = random.sample(fortunes, count)
        
        self.__open_data()
        cookies = []
        data = self.data
        for offset, length in sample:
            data.seek(offset, 0)
            cookies.append(data.read(length).decode('utf-8', 'replace').rstrip('\r\n'))
        return cookies[0] if count == 1 else cookies
    
    def close(self):
        if self.data is not None:
            self.data.close()
        self.compiled.close()
    __del__ = close
    
    def __unicode__(self):
        if self.compiled_path is not None:
            return '<Compiled Fortune File: Path: %s>' % self.compiled_path
        return '<Compiled Fortune File: %s>' % self.compiled
    
    if int(sys.version[0]) > 2:
        __str__ = __unicode__
    else:
        def __str__(self):
            return unicode(self).encode('mbcs' if os.name == 'nt' else 'utf-8', 'xmlcharrefescape')
