from pyfortune.FortuneFile import FortuneFile
from pyfortune.path import list_fortune, fortunepath
from io import open

import random

def load_all(offensive=None, path=None):
    if path is None:
        path = fortunepath
    else:
        path.extend(fortunepath)
    for file in list_fortune(offensive, path):
        yield FortuneFile(open(file, encoding='utf-8'))

class Chooser(object):
    def __init__(self, offensive=None, path=None):
        self.choices = choices = []
        for fortune in load_all(offensive, path):
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
