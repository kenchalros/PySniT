from .vscode import get_vscode_snippet_dirpath, get_vscode_snippet_filepath
import shutil
import json
import os
import sys


class SnippetFileIO:
    """Snippetの書き込み,削除,バックアップ等の操作を行う.
    """

    def __init__(self):
        pass

    def backup(self) -> None:
        """Back up snippet file.
        """
        if not self.is_python_json_exists('python.json'):
            print("`python.json` to back up doesn't exist.")
            return

        if self.is_python_json_exists('python_backup.json'):
            print("`python_backup.json` already exists.")
            print("Update backup file?")
            dic = {'y': True, 'yes': True, 'n': False, 'no': False}
            ans = False
            while True:
                ans = input('[Y]es/[N]o? >> ').lower()
                if ans in dic:
                    ans = dic[ans]
                    break
                print('Error! Input again.')
            if ans:
                self.backup_snippet_file()
                print("Update backup file.")
        else:
            self.backup_snippet_file()
            print("Created backup file `python_backup.json`.")

    def backup_snippet_file(self):
        src_filepath = get_vscode_snippet_filepath('python.json')
        dist_filepath = get_vscode_snippet_filepath(
            'python_backup.json')
        shutil.copy(src_filepath, dist_filepath)

    def write_snippets_in_vscode_file(self, snippet_dict):
        """Write snippet into vscode setting file.
        """
        python_snippet_file = get_vscode_snippet_filepath('python.json')
        with open(python_snippet_file, 'w') as f:
            json.dump(snippet_dict, f, indent='\t')

    def is_python_json_exists(self, filename):
        python_snippet_file = get_vscode_snippet_filepath(filename)
        if os.path.isfile(python_snippet_file):
            return True
        else:
            return False
