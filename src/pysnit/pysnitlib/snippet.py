from inspect import getsource, getdoc

from typing import NamedTuple
from typing import List, Dict, Tuple, Any, Callable, Optional
from functools import wraps
import warnings
from .utils import remove_decorator


class SnippetType(NamedTuple):
    name: str
    prefix: str
    body: str
    description: Optional[str]


class snippet:
    """スニペットマーカー用クラス
    """
    snippets: List[SnippetType] = []

    def __init__(self, *args, **kwargs) -> None:
        # print()
        # print("called __init__ with args:", args, "kwargs:", kwargs)
        self._obj = None
        self._args: Tuple[Any, ...] = ()
        self._kwargs: Dict[str, Any] = {}
        if len(args) == 1 and callable(args[0]):
            self._obj = self._my_decorator(args[0])
        else:
            self._args = args
            self._kwargs = kwargs

    def __call__(self, *args, **kwargs) -> Any:
        # print( "called __call__ with args:", args, "kwargs:", kwargs )
        if self._obj is None:
            if len(args) == 1 and callable(args[0]):
                self._obj = self._my_decorator(args[0])
                return self._obj
        else:
            try:
                ret = self._obj(*args, **kwargs)
            except:
                raise
            return ret

    def _my_decorator(self, obj: Callable) -> Callable:
        # print("called _my_decorator with obj:", obj)

        # snippet register
        self._check_snippet_option()
        snippet = self._make_snippet(obj)
        self._add_snippet(snippet)

        @wraps(obj)
        def wrapper(*args, **kwargs):
            try:
                ret = obj(*args, **kwargs)
            except:
                raise
            return ret
        return wrapper

    def _make_snippet(self, obj: Callable) -> SnippetType:
        """
        """
        name: str = self._kwargs['name'] if 'name' in self._kwargs else obj.__name__
        prefix: str = self._kwargs['prefix'] if 'prefix' in self._kwargs else obj.__name__
        description: Optional[str] = self._kwargs['description'] if 'description' in self._kwargs else None
        srccode: str = remove_decorator(getsource(obj), '@snippet')
        snippet = SnippetType(name, prefix, srccode, description)
        return snippet

    def _add_snippet(self, snippet: SnippetType) -> None:
        """srccodeをsnippetsに追加する
        """
        self.__class__.snippets.append(snippet)

    def _check_snippet_option(self):
        """snippetデコレータのオプションをチェックする.
        想定外のオプションが指定されている場合warningメッセージを表示する.
        """
        item_keys = ['name', 'prefix', 'description']
        for key in self._kwargs.keys():
            if not key in item_keys:
                warnings.warn('`{}` is not valid argument.'.format(key))
                warnings.warn(
                    'Valid arguments ars `prefix` and `description`.')
