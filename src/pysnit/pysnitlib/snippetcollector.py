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


class SnippetCollector:
    """A class that manages snippets by snippet decorator.
    """

    def __init__(self, filepath):
        self.dict_toml = self._read_snippet_file(filepath)
        self.module_snippets = None
        self.inline_snippets = None
        self.dict_snippets: SnippetDict = {}

    def register_snippets(self):
        self.load_snippets_from_toml()
        self._set_snippets_into_dict()
        self._print_snippets()
        self.write_snippets_in_vscode_file()

    def _set_snippets_into_dict(self):
        self._module_snippets_to_dict()
        self._inline_snippets_to_dict()

    def _read_snippet_file(self, snippet_filepath):
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

    def load_snippets_from_toml(self):
        """Load snippets from dict_toml and then set.
        :param dict_toml: snippet file content
        """
        # 'module' snippets will be dynamically imported.
        # other inline snippets will be read as it is.
        try:
            modules = self.dict_toml.pop('module')
        except KeyError as e:
            @errmsghandler(e)
            def _errmsg():
                print("toml setting file MUST contain ['module'] section.")
            _errmsg()
        for modulename, modulepath in modules.items():
            # This `module` variable is overwrited each iteration, but it's OK.
            module = utils.load_module_from_path(modulename, modulepath)
        self.module_snippets = module.snippet.snippets
        self.inline_snippets = self.dict_toml

    def _transform_body_for_vscode(self, body: str) -> List[str]:
        """snippetのbodyをvscode用に変換する.
        改行区切りのlist, space4つをtabに変換.
        :param body: string of a snippet body
        :return body_for_vscode: vscode-snippet形式のbody
        """
        body_list = body.split('\n')
        body_for_vscode = [b.replace('    ', '\t') for b in body_list]
        return body_for_vscode

    def _module_snippets_to_dict(self):
        """Set module snippet content to snippet dict.
        """
        for snippet in self.module_snippets:
            name, prefix, body, description = snippet
            content = {}
            content['prefix']: str = prefix
            content['body']: List[str] = self._transform_body_for_vscode(body)
            if description is not None:
                content['description']: str = description
            self.dict_snippets[name] = content

    def _inline_snippets_to_dict(self):
        """Set inline snippet content to snippet dict.
        if `prefix` is empty, the value will be filled with name automatically.
        raise exception if `body` doesn't exist in content.
        """
        try:
            for name, content in self.inline_snippets.items():
                if not 'body' in content.keys():
                    raise NotFoundBodyKey()
                if not 'prefix' in content.keys():
                    content['prefix']: str = name
                self.dict_snippets[name] = content
        except NotFoundBodyKey as e:
            @errmsghandler(e)
            def _errmsg():
                print("`inline snippet` MUST have 'body'.")
                print(
                    "However, [{}] doesn't have one in the snippet setting file.".format(name))
            _errmsg()
            exit(1)

    def to_json(self):
        print(json.dumps(self.dict_snippets, indent='\t'))

    def write_snippets_in_vscode_file(self):
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
                json.dump(self.dict_snippets, f, indent='\t')
        except IOError as e:
            print('{}: {}'.format(e.__class__.__name__, e))
            exit(1)

    def _print_snippets(self):
        names = self.dict_snippets.keys()
        print('[snippet num]')
        print(len(names))
        print('[names]')
        for name in names:
            print('- {}'.format(name))
