from pyfortune.FortuneFile import FortuneFile
from pyfortune.compile import sthead, stentry
import struct
import os
import io
import random

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
        self = cls.__new__()
        self.compiled_path = compiled_path
        self.data_path = data_path
        self.data = data
        self.compiled = compiled
        self.mtime = 0
        self.__load_compiled()
    
    def __load_compiled(self):
        file = self.compiled
        self.version, self.size, self.flags, mtime = sthead.unpack(file.read(sthead.size))
        if self.version != 0xDEADFACE:
            raise ValueError('Compiled file of the future!')
        if mtime < self.mtime:
            raise ValueError('Outdated compiled file')
        self.fortunes = fortunes = []
        while True:
            read = file.read(stentry.size)
            if not read:
                break
            fortunes.append(stentry.unpack(read))
        if len(self.fortunes) != self.size:
            raise ValueError("Your file doesn't have the same size as it described itself to have")
        file.close()
    
    def __open_data(self):
        if self.data is None:
            self.data = io.open(self.data_path)
    
    def choose(self, long=None, size=160, count=1):
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
            cookies.append(data.read(length).rstrip('\r\n'))
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
    
    def __str__(self):
        return unicode(self).encode('mbcs' if os.name == 'nt' else 'utf-8', 'xmlcharrefescape')
