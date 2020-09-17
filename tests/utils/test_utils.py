import sys
import os
import pytest
import pysnit.pysnitlib.utils as utils
from . import sample
import inspect

class TestUtils:

    def test_load_module_from_path(self):
        """'load_module_from_path'で読み込んだsampleモジュールと
        直接importしたsampleモジュールのソースが同じかどうかをチェック.
        """
        # set module path
        self_path = os.path.abspath(__file__)
        dirpath_of_self = os.path.dirname(self_path)
        module_path = os.path.abspath(dirpath_of_self + '/sample.py')
        # load module
        module = utils.load_module_from_path('sample', module_path)
        # check
        actual_src = inspect.getsource(module)
        expected_src = inspect.getsource(sample)
        assert actual_src == expected_src

    def test_remove_decorator(self):
        """@snippetデコレータを取り除く.
        """
        targets = [
"""@snippet(prefix='sample_1',
        description='This snippet prefix is `sample1_1.`')
def sample1_prefix_and_description():
    pass
""",
"""@snippet
def no_snippet_option():
    pass
""",
"""def no_snippet_marker():
    pass
""",
        ]

        expected_results = [
"""def sample1_prefix_and_description():
    pass""",
"""def no_snippet_option():
    pass""",
"""def no_snippet_marker():
    pass""",
        ]

        actual_results = [utils.remove_decorator(t, '@snippet') for t in targets]
        for actual, expected in zip(actual_results, expected_results):
            assert actual == expected
