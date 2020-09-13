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
        actualsrc = inspect.getsource(module)
        expectedsrc = inspect.getsource(sample)
        assert actualsrc == expectedsrc
