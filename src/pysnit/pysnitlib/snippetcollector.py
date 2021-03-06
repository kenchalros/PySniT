import os
from . import utils
import toml
import json
from .vscode import get_vscode_snippet_dirpath
from .errors import NotFoundBodyKey, errmsghandler
from .funcs import f_chain
from .types import SnippetType, ModuleSnippet, InlineSnippet, SnippetData, SnippetContent, SnippetDict
from typing import List, Dict, NoReturn, Union


def register_snippets(filepath: str) -> SnippetDict:
    """Register snippets from snippet setting file.
    :param filepath: snippet setting toml.
    """
    snippet_dict = f_chain(filepath,
                           _read_snippet_file,
                           _load_snippets_from_toml,
                           _convert_snippets_to_dict)
    _print_snippets(snippet_dict)
    return snippet_dict


def _convert_snippets_to_dict(snippets: SnippetData) -> SnippetDict:
    """
    :param snippets
    :return dict of snippets
    """
    dict_module_snippets = _module_snippets_to_dict(snippets.module)
    dict_inline_snippets = _inline_snippets_to_dict(snippets.inline)
    return {**dict_module_snippets, **dict_inline_snippets}


def _read_snippet_file(snippet_filepath: str):
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


def _load_snippets_from_toml(dict_toml: Dict) -> SnippetData:
    """Load snippets from dict_toml and then set.
    :param dict_toml: snippet file content
    """
    # 'module' snippets will be dynamically imported.
    # other 'inline' snippets will be read as it is.
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

    return SnippetData(module_snippets, inline_snippets)


def _transform_body_for_vscode(body: str) -> List[str]:
    """snippetのbodyをvscode用に変換する.
    改行区切りのlist, space4つをtabに変換.
    :param body: string of a snippet body
    :return body_for_vscode: vscode-snippet形式のbody
    """
    body_list = body.split('\n')
    body_for_vscode = [b.replace('    ', '\t') for b in body_list]
    return body_for_vscode


def _module_snippets_to_dict(module_snippets: List[SnippetType]) -> SnippetDict:
    """Set module snippet content to snippet dict.
    :param module_snippets
    :return snippets converted dict format
    """
    dict_snippets: SnippetDict = {}
    for snippet in module_snippets:
        name, prefix, body, description = snippet
        content: SnippetContent = {
            'prefix': prefix,
            'body': _transform_body_for_vscode(body),
            'description': description,
        }
        dict_snippets[name] = content
    return dict_snippets


def _inline_snippets_to_dict(inline_snippets: InlineSnippet) -> Union[SnippetDict, NoReturn]:
    """Set inline snippet content to snippet dict.
    if `prefix` is empty, the value will be filled with name automatically.
    :param inline_snippets: 
    :return dict_snippets: 
    :error NotFoundBodyKey: if `body` doesn't exist in content, raise NotFoundBodyKey error.
    """
    try:
        dict_snippets: SnippetDict = {}
        for name, content in inline_snippets.items():
            if not 'body' in content.keys():
                raise NotFoundBodyKey()
            if not 'prefix' in content.keys():
                content['prefix'] = name
            dict_snippets[name] = {
                'prefix': content['prefix'],
                'body': content['body'],
                'description': 'hoge'
            }
        return dict_snippets
    except NotFoundBodyKey as e:
        @errmsghandler(e)
        def _errmsg():
            print("`inline snippet` MUST have 'body'.")
            print(
                "However, [{}] doesn't have one in the snippet setting file.".format(name))
        _errmsg()
        exit(1)


def _print_snippets(dict_snippets: SnippetDict) -> None:
    names = dict_snippets.keys()
    print('[snippet num]')
    print(len(names))
    print('[names]')
    for name in names:
        print('- {}'.format(name))
