from pyfortune.FortuneFile import FortuneFile
from pyfortune.CompiledFortuneFile import CompiledFortuneFile
from pyfortune.path import list_fortune, fortunepath
from io import open

import logging
import os
import random

logger = logging.getLogger('pyfortune')

def load_all(offensive=None, path=None):
    if path is None:
        path = fortunepath
    else:
        path.extend(fortunepath)
    for file in list_fortune(offensive, path):
        if os.path.isfile(file + '.ftc'): # ForTune Compiled
            try:
                logger.debug("Trying compiled file: %s", file + '.ftc')
                yield CompiledFortuneFile(file + '.ftc')
            except ValueError as e:
                logger.warning("Can't use compiled file: %s: %s", file + '.ftc', e)
            else:
                continue
        fortune = FortuneFile(open(file, 'rb'))
        logging.info('Compiling: %s', file)
        fortune.compile(open(file + '.ftc', 'wb'))
        yield fortune

class Chooser(object):
    def __init__(self, offensive=None, path=None):
        self.choices = choices = []
        for fortune in load_all(offensive, path):
            #print fortune, fortune.size
            choices.extend([fortune] * fortune.size)
    
    def choose_file(self):
        return random.choice(self.choices)
    
    def choose(self, long=None, size=160, recurse=0):
        file = self.choose_file()
        if recurse > 20:
            # What a bad luck, or may be you just can't find it
            return None
        choice = file.choose(long, size)
        if choice is None:
            choice = self.choose(long, size, recurse+1)
        return choice
