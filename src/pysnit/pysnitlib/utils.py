from importlib.util import spec_from_file_location, module_from_spec
from importlib.abc import Loader
import sys
import importlib
from .errors import errmsghandler


def load_module_from_path(module_name: str, module_path: str):
    """dynamically import module from module name and file path.
    :param module_name: module name
    :param module_path: module file path
    :return module: imported module
    """
    try:
        spec = spec_from_file_location(module_name, module_path)
        module = module_from_spec(spec)
        sys.modules[module_name] = module

        # This assert statement needed for fix below error with mypy.
        # error message:
        #   error: Item "_Loader" of "Optional[_Loader]" has no attribute "exec_module"
        #   error: Item "None" of "Optional[_Loader]" has no attribute "exec_module"
        # reference link:
        #   https://github.com/python/typeshed/issues/2793
        assert isinstance(spec.loader, Loader)

        spec.loader.exec_module(module)
        return module
    except FileNotFoundError as e:
        @errmsghandler(e)
        def _errmsg():
            print('Module path may be wrong in the snippet setting file.')
            print("Please fix '{}'.".format(module_path))
        _errmsg()


def remove_decorator(srccode: str, decorator: str) -> str:
    """remove decorator from return value of `inspect.getsource`.
    :param srccode: return value of `inspect.getsource`
    :param decorator: remove target ex: '@snippet'
    :return srccode_without_decorator: srccode removed decorator
    """
    # no decorator remained
    if srccode.find(decorator) != 0:
        return srccode.strip()

    len_deco = len(decorator)
    # no option
    if srccode[len_deco] != '(':
        return srccode[len_deco:].strip()

    stack = []
    stack.append('(')
    i = len_deco + 1
    while stack:
        top = stack[-1]
        nchr = srccode[i]
        if top == '(':
            if nchr == ')':
                stack.pop()
            elif nchr == "'" or nchr == '"':
                stack.append(nchr)
        elif top == "'":
            if nchr == "'":
                stack.pop()
        elif top == '"':
            if nchr == '"':
                stack.pop()
        i += 1

    return srccode[i:].strip()
