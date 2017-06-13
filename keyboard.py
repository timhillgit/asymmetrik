"""Test suite:

>>> ac = AutocompleteProvider()
>>> ac.train("The third thing that I need to tell you is that this thing does not think thoroughly.")
>>> ac.getWords("thi")
["thing" (2), "think" (1), "third" (1), "this" (1)]
>>> ac.getWords("nee")
["need" (1)]
>>> ac.getWords("th")
["that" (2), "thing" (2), "think" (1), "this" (1), "third" (1), "the" (1), "thoroughly" (1)]
"""

from collections import namedtuple

class Candidate(namedtuple('Candidate', ['word', 'confidence'])):
    def getWord(self):
        """Returns the autocomplete candidate."""
        return self.word

    def getConfidence(self):
        """Returns the confidence for the candidate."""
        return self.confidence

    def __str__(self):
        return '"{self.word}" ({self.confidence})'.format(self=self)

class AutocompleteProvider:
    def __init__(self, source=None):
        """Create an AutocompleteProvider.

        If source is provided, it is a file-like object used to train.
        """
        if source:
            self.train(source.read())

    def getWords(self, fragment):
        """Returns list of candidates ordered by confidence."""
        pass

    def train(self, passage):
        """Trains the algorithm with the provided passage."""
        pass

if __name__ == '__main__':
    pass
