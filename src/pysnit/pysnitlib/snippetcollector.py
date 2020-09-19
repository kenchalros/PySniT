import os
from . import utils
import toml
import json
from typing import List
from .snippet import SnippetType
from typing_extensions import TypedDict
from typing import Optional


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
        self.write_snippets_in_vscode_file()

    def _set_snippets_into_dict(self):
        self._module_snippets_to_dict()
        self._inline_snippets_to_dict()

    def _read_snippet_file(self, snippet_filepath):
        """Read snippet manage file and then set dict_toml
        :param snippet_filepath: snippet file path
        :return dict_toml: readed toml dict
        """
        dict_toml = None
        with open(snippet_filepath, 'r') as f:
            dict_toml = toml.load(f)
        return dict_toml

    def load_snippets_from_toml(self):
        """Load snippets from dict_toml and then set.
        :param dict_toml: snippet file content
        """
        # TODO: keyが存在しない場合等へのエラー処理を追加する
        # 'module' snippets will be dynamically imported.
        # other inline snippets will be read as it is.
        modules = self.dict_toml.pop('module')
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
        """
        for name, content in self.inline_snippets.items():
            if not 'prefix' in content.keys():
                content['prefix']: str = name
            self.dict_snippets[name] = content

    def to_json(self):
        print(json.dumps(self.dict_snippets, indent='\t'))

    def write_snippets_in_vscode_file(self):
        """write snippet into vscode snippet file.
        `python.json` which already exists will be renamed to `python_old.json`
        """
        vscode_snippet_dir: str = self._get_vscode_snippet_dirpath()
        python_snippet = vscode_snippet_dir + 'python.json'
        if os.path.isfile(python_snippet):
            os.rename(python_snippet, vscode_snippet_dir + '/python_old.json')

        with open(python_snippet, 'w') as f:
            json.dump(self.dict_snippets, f, indent='\t')

    def _get_vscode_snippet_dirpath(self) -> str:
        """Get a path of vscode snippet directory.
        :return vscode_snippet_dir: a path of vscode snippet directory
        """
        homedir = os.environ['HOME']
        vscode_snippet_dir = homedir + '/Library/Application Support/Code/User/snippets/'
        return vscode_snippet_dir
