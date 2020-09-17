import sys
import os
import pytest
from pysnit.pysnitlib.snippetcollector import SnippetCollector
from pysnit.pysnitlib import utils

# mock of snippet path file
dict_toml = {
    'snippet': {
        # These paths are set assuming that they will be executed
        # from the project root during testing.
        # So, `.` represents the path of this project root.
        'sample1': './tests/snippetcollector/sample_modules/sample1.py',
        'sample2': './tests/snippetcollector/sample_modules/sample2.py'
    }
}
abspath_sample1 = os.path.abspath(dict_toml['snippet']['sample1'])
abspath_sample2 = os.path.abspath(dict_toml['snippet']['sample2'])
dict_toml['snippet']['sample1'] = abspath_sample1
dict_toml['snippet']['sample2'] = abspath_sample2

class TestSnippetCollector:

    def test_read_snippet_pathfile(self):
        """read_snippet_pathfileを呼び出すとdict_tomlに読みだしたdictがセットされる
        """
        SC = SnippetCollector()
        assert SC.dict_toml is None
        SC.read_snippet_pathfile('./tests/snippetcollector/samplepath.toml')
        assert SC.dict_toml is not None

    def test_load_snippets(self):
        """dict_tomlにセットされたモジュールのパスからモジュールをロードし、snippet指定された
        関数、クラス等をsnippetとして取り出す。
        """

        # mocking
        SC = SnippetCollector()
        SC.dict_toml = dict_toml

        assert SC.snippets is None
        SC.load_snippets()
        assert SC.snippets is not None

        SC.to_dict()
        print()
        SC.to_json()