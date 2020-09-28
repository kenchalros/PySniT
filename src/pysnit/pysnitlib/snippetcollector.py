import os
from . import utils
import toml
import json
from typing import List
from .snippet import SnippetType
from .vscode import get_vscode_snippet_dirpath
from typing_extensions import TypedDict
from typing import Optional
from .errorhandle import errmsghandler
from .error import NotFoundBodyKey


class SnippetDict(TypedDict):
    name: str


class Snippet(TypedDict):
    prefix: str
    body: str
    description: Optional[str]


def register_snippets(filepath):
    dict_toml = _read_snippet_file(filepath)
    module_snippets, inline_snippets = load_snippets_from_toml(dict_toml)
    dict_snippets = _set_snippets_into_dict(module_snippets, inline_snippets)
    _print_snippets(dict_snippets)
    write_snippets_in_vscode_file(dict_snippets)

def _set_snippets_into_dict(module_snippets, inline_snippets):
    dict_snippets = {}
    dict_module_snippets = _module_snippets_to_dict(module_snippets)
    dict_inline_snippets = _inline_snippets_to_dict(inline_snippets)

    dict_snippets.update(dict_module_snippets)
    dict_snippets.update(dict_inline_snippets)
    return dict_snippets

def _read_snippet_file(snippet_filepath):
    """Read snippet manage file and then set dict_toml
    :param snippet_filepath: snippet file path
    :return dict_toml: readed toml dict
    """
    try:
        dict_toml = None
        with open(snippet_filepath, 'r') as f:
            dict_toml = toml.load(f)
        return dict_toml
    except FileNotFoundError as e:
        @errmsghandler(e)
        def _errmsg():
            print(
                "If you don't have 'snippet.toml' on current working directory, please create it.")
            print("If you have another name file, please use '--file' option.")
            print("You can find details with the command 'pysnit help'.")
        _errmsg()
    except IOError as e:
        raise e

def load_snippets_from_toml(dict_toml):
    """Load snippets from dict_toml and then set.
    :param dict_toml: snippet file content
    """
    # 'module' snippets will be dynamically imported.
    # other inline snippets will be read as it is.
    try:
        modules = dict_toml.pop('module')
    except KeyError as e:
        @errmsghandler(e)
        def _errmsg():
            print("toml setting file MUST contain ['module'] section.")
        _errmsg()
    for modulename, modulepath in modules.items():
        # This `module` variable is overwrited each iteration, but it's OK.
        module = utils.load_module_from_path(modulename, modulepath)

    module_snippets = module.snippet.snippets
    inline_snippets = dict_toml
    return module_snippets, inline_snippets

def _transform_body_for_vscode(body: str) -> List[str]:
    """snippetのbodyをvscode用に変換する.
    改行区切りのlist, space4つをtabに変換.
    :param body: string of a snippet body
    :return body_for_vscode: vscode-snippet形式のbody
    """
    body_list = body.split('\n')
    body_for_vscode = [b.replace('    ', '\t') for b in body_list]
    return body_for_vscode

def _module_snippets_to_dict(module_snippets):
    """Set module snippet content to snippet dict.
    """
    dict_snippets = {}
    for snippet in module_snippets:
        name, prefix, body, description = snippet
        content = {}
        content['prefix']: str = prefix
        content['body']: List[str] = _transform_body_for_vscode(body)
        if description is not None:
            content['description']: str = description
        dict_snippets[name] = content
    return dict_snippets

def _inline_snippets_to_dict(inline_snippets):
    """Set inline snippet content to snippet dict.
    if `prefix` is empty, the value will be filled with name automatically.
    raise exception if `body` doesn't exist in content.
    """
    try:
        dict_snippets = {}
        for name, content in inline_snippets.items():
            if not 'body' in content.keys():
                raise NotFoundBodyKey()
            if not 'prefix' in content.keys():
                content['prefix']: str = name
            dict_snippets[name] = content
        return dict_snippets
    except NotFoundBodyKey as e:
        @errmsghandler(e)
        def _errmsg():
            print("`inline snippet` MUST have 'body'.")
            print(
                "However, [{}] doesn't have one in the snippet setting file.".format(name))
        _errmsg()
        exit(1)

def write_snippets_in_vscode_file(dict_snippets):
    """write snippet into vscode snippet file.
    `python.json` which already exists will be renamed to `python_old.json`
    """
    vscode_snippet_dir: str = get_vscode_snippet_dirpath()
    python_snippet = vscode_snippet_dir + 'python.json'
    try:
        if os.path.isfile(python_snippet):
            os.rename(python_snippet, vscode_snippet_dir +
                        '/python_old.json')
        with open(python_snippet, 'w') as f:
            json.dump(dict_snippets, f, indent='\t')
    except IOError as e:
        print('{}: {}'.format(e.__class__.__name__, e))
        exit(1)

def _print_snippets(dict_snippets):
    names = dict_snippets.keys()
    print('[snippet num]')
    print(len(names))
    print('[names]')
    for name in names:
        print('- {}'.format(name))
