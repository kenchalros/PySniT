from inspect import getsource, getdoc
from functools import wraps
import warnings
from .utils import remove_decorator
from .types import SnippetType
from typing import Tuple, List, Dict, Optional, Callable, Any


class snippet:
    """This class is snippet decorator.
    Decorated methods or classes will be registerd as snippets.

    how to use:
    ```python
    @snippet
    def sample():
        ...

    @snippet(name='sample', prefix='s', description='sample method')
    def sample2():
        ...

    @snippet(prefix='sc')
    class Sample:
        ...
    ```
    """
    snippets: List[SnippetType] = []

    def __init__(self, *args, **kwargs) -> None:
        self._obj = None
        self._args: Tuple[Any, ...] = ()
        self._kwargs: Dict[str, Any] = {}
        if len(args) == 1 and callable(args[0]):
            self._obj = self._decorator(args[0])
        else:
            self._args = args
            self._kwargs = kwargs

    def __call__(self, *args, **kwargs) -> Any:
        if self._obj is None:
            if len(args) == 1 and callable(args[0]):
                self._obj = self._decorator(args[0])
                return self._obj
        else:
            try:
                ret = self._obj(*args, **kwargs)
            except:
                raise
            return ret

    def _decorator(self, obj: Callable) -> Callable:
        self._register_snippet(obj)

        @wraps(obj)
        def wrapper(*args, **kwargs):
            try:
                ret = obj(*args, **kwargs)
            except:
                raise
            return ret
        return wrapper

    def _register_snippet(self, obj: Callable):
        self._check_snippet_option()
        snippet = self._make_snippet(obj)
        self._add_snippet(snippet)

    def _make_snippet(self, obj: Callable) -> SnippetType:
        """make snippet obj.
        Default value of `name` and `prefix` is object name.
        :param obj: decorated Callable obj
        :return snippet
        """
        name: str = self._kwargs['name'] if 'name' in self._kwargs else obj.__name__
        prefix: str = self._kwargs['prefix'] if 'prefix' in self._kwargs else obj.__name__
        srccode: str = remove_decorator(getsource(obj), '@snippet')
        description: Optional[str] = self._kwargs['description'] if 'description' in self._kwargs else None
        return SnippetType(name, prefix, srccode, description)

    def _add_snippet(self, snippet: SnippetType) -> None:
        """add srccode into snippets
        :param snippet: snippet to be added
        """
        self.__class__.snippets.append(snippet)

    def _check_snippet_option(self):
        """Check options of snippet decorator.
        If unsupported option is assigned, show warning messages.
        """
        item_keys = ['name', 'prefix', 'description']
        for key in self._kwargs.keys():
            if not key in item_keys:
                warnings.warn('`{}` is not valid argument.'.format(key))
                warnings.warn(
                    'Valid arguments ars `name`, `prefix` and `description`.')
