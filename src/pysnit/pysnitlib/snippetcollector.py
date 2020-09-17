from . import utils
import toml
import json


class SnippetCollector:

    def __init__(self):
        self.dict_toml = None
        self.snippets = None
        self.dict_snippets = {}

    def get_toml(self):
        return self.dict_toml

    def read_snippet_pathfile(self, filepath):
        """Read toml file and then set dict_toml
        :param filepath: path to toml file
        """
        with open(filepath, 'r') as f:
            self.dict_toml = toml.load(f)

    def load_snippets(self):
        """Load snippets from dict_toml and then set snippets.
        """
        snippets = self.dict_toml['snippet']
        for modulename, modulepath in snippets.items():
            # This `module` variable is overwrited each iteration, but it's OK.
            module = utils.load_module_from_path(modulename, modulepath)
        self.snippets = module.snippet.snippets

    def transform_body_for_vscode(self, body):
        body_list = body.split('\n')
        body_list_space_to_tab = [b.replace('    ', '\t') for b in body_list]
        return body_list_space_to_tab

    def to_dict(self):
        for snippet in self.snippets:
            name, prefix, body, description = snippet
            content = {}
            content['prefix'] = prefix
            content['body'] = self.transform_body_for_vscode(body)
            if description is not None:
                content['description'] = description
            self.dict_snippets[name] = content

    def to_json(self):
        print(json.dumps(self.dict_snippets, indent='\t'))
