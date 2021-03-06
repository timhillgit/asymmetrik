#!/usr/bin/env python3
"""Test suite:

>>> ac = AutocompleteProvider()
>>> ac.train("The third thing that I need to tell you is that this thing does not think thoroughly.")
>>> thi = ac.getWords("thi")
>>> print (*thi, sep=', ')
"thing" (2), "this" (1), "third" (1), "think" (1)
>>> nee = ac.getWords("nee")
>>> print (*nee, sep=', ')
"need" (1)
>>> th = ac.getWords("th")
>>> print (*th, sep=', ')
"thing" (2), "that" (2), "thoroughly" (1), "this" (1), "third" (1), "think" (1), "the" (1)
>>> ac.getWords("foo")
[]
>>> ac.getWords("")
[]
"""

from collections import namedtuple, Counter
from string import punctuation
from functools import total_ordering
import sys
import pygtrie

@total_ordering
class Candidate(namedtuple('Candidate', ['word', 'confidence'])):
    def getWord(self):
        """Returns the autocomplete candidate."""
        return self.word

    def getConfidence(self):
        """Returns the confidence for the candidate."""
        return self.confidence

    def __str__(self):
        return '"{self.word}" ({self.confidence})'.format(self=self)

    def __lt__(self, other):
        try:
            return (self.confidence, self.word) < (other.confidence, other.word)
        except AttributeError:
            return NotImplemented

class AutocompleteProvider:
    def __init__(self, source=None):
        """Create an AutocompleteProvider.

        If source is provided, it is a file-like object used to train.
        """
        self.trie = pygtrie.CharTrie()
        if source:
            self.train(source.read())

    def getWords(self, fragment):
        """Returns list of candidates ordered by confidence."""
        if not fragment or not self.trie.has_subtrie(fragment):
            return []
        results = self.trie.items(prefix=fragment.lower())
        candidates = (Candidate(*item) for item in results)
        return sorted(candidates, reverse=True)

    def train(self, passage):
        """Trains the algorithm with the provided passage."""
        words = (word.lower().strip(punctuation) for word in passage.split())
        for word, count in Counter(words).items():
            confidence = self.trie.get(word, 0)
            confidence += count
            self.trie[word] = confidence

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: keyboard.py training_file")
    with open(sys.argv[1], 'r') as training_file:
        ac = AutocompleteProvider(training_file)
    for line in sys.stdin:
        candidates = ac.getWords(line.strip())[:4]
        print(*candidates, sep=', ')
