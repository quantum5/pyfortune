from __future__ import division
from pyfortune.FortuneFile import FortuneFile
from pyfortune.CompiledFortuneFile import CompiledFortuneFile
from pyfortune.path import list_fortune, fortunepath
from io import open
from operator import attrgetter

import logging
import os
import random

logger = logging.getLogger('pyfortune')

def _load_fortune(file):
    compiled = file + '.ftc' # ForTune Compiled
    if os.path.isfile(compiled):
        try:
            logger.debug("Trying compiled file: %s", compiled)
            return CompiledFortuneFile(compiled)
        except ValueError as e:
            logger.warning("Can't use compiled file: %s: %s", compiled, e)
    fortune = FortuneFile(open(file, 'rb'))
    logging.info('Compiling: %s', file)
    fortune.compile(open(compiled, 'wb'))
    return fortune

def load_fortune(file, path=None, offensive=False):
    if os.path.isabs(file):
        return _load_fortune(file)
    if path is None:
        path = fortunepath
    else:
        path = path[:]
        path.extend(fortunepath)
    for dir in path:
        if offensive:
            test = os.path.join(dir, 'off', file)
        else:
            test = os.path.join(dir, file)
        if os.path.isfile(test):
            return _load_fortune(test)
        elif offensive is None:
            test = os.path.join(dir, 'off', file)
            print test
            if os.path.isfile(test):
                return _load_fortune(test)

def load_all(offensive=False, path=None):
    if path is None:
        path = fortunepath
    else:
        path.extend(fortunepath)
    for file in list_fortune(offensive, path):
        yield _load_fortune(file)

class Chooser(object):
    def __init__(self, offensive=None, path=None, equal=False):
        """Initialize based on all available fortune files"""
        # Let me explain:
        # files is a list of tuples (fortune, upper bound)
        # fortune is the file object, upper bound is the maximum number that will
        # result in this file being chosen, that has not been chosen by previous
        # files. It's important that upper bound increases when index in files
        # increases
        self.files = files = []
        count = 0
        for fortune in load_all(offensive, path):
            count += 1 if equal else fortune.size
            files.append((fortune, count))
        self.count = count
    
    @classmethod
    def fromlist(cls, files, equal=False, offensive=False):
        """Initialize based on a list of fortune files"""
        self = cls.__new__(cls)
        self.files = fortunes = []
        count = 0
        for file in files:
            fortune = load_fortune(file, offensive=offensive)
            if fortune is None:
                logger.warn("Can't load: %s", file)
                continue
            count += 1 if equal else fortune.size
            fortunes.append((fortune, count))
        if not fortunes:
            raise ValueError('All fortune files specified are invalid')
        self.count = count
        return self
    
    def choose_file(self):
        number = random.randrange(self.count)
        for file, prob in self.files:
            if prob > number:
                return file
        raise RuntimeError('No fortune???')
    
    def choose(self, long=None, size=160, recurse=0):
        if recurse > 20:
            # What a bad luck, or may be you just can't find it
            return None
        file = self.choose_file()
        choice = file.choose(long, size)
        if choice is None:
            file, choice = self.choose(long, size, recurse+1)
        return file, choice
