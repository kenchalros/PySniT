import sys
import os
import pytest
from pysnit.pysnitlib.snippet import snippet
from pysnit.pysnitlib.snippet import SnippetType
from . import sample

@snippet
def sample0():
    pass

@snippet(name='snippet_sample1', prefix='s1')
def sample1():
    pass

@snippet(prefix='s2', description='This is sample2 method.')
def sample2():
    pass

class TestSnippet:

    def test_snippet_decorator(self):
        """snippetデコレータをつけることでモジュールが収集される.
        prefixの指定がない場合、モジュール名がそのままprefixになる.
        descriptionは指定しない場合Noneになる.
        """
        snippet_obj = snippet()

        actual0 = snippet_obj.snippets[0]
        expected0 = SnippetType('sample0','sample0', 'def sample0():\n    pass', None)
        assert actual0 == expected0

        actual1 = snippet_obj.snippets[1]
        expected1 = SnippetType('snippet_sample1', 's1', 'def sample1():\n    pass', None)
        assert actual1 == expected1

        actual2 = snippet_obj.snippets[2]
        expected2 = SnippetType('sample2', 's2', 'def sample2():\n    pass', 'This is sample2 method.')
        assert actual2 == expected2

