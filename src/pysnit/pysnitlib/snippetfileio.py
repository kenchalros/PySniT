from .vscode import get_vscode_snippet_dirpath, get_vscode_snippet_filepath
import shutil
import json
import os
import sys


def yes_or_no() -> bool:
    while True:
        ans = input('[Y]es/[N]o? >> ').lower()
        if ans in ('y', 'yes', 'n', 'no'):
            return ans.startswith('y')
        print('Error! Input again.')


SNIPPET_FILE = 'python.json'
BACKUP_FILE = 'python_backup.json'


def backup() -> None:
    """Back up snippet file.
    """
    if not is_python_json_exists(SNIPPET_FILE):
        print("`{}` to back up doesn't exist.".format(SNIPPET_FILE))
        return

    if is_python_json_exists(BACKUP_FILE):
        print("`{}` already exists.".format(BACKUP_FILE))
        print("Update backup file?")
        ans = yes_or_no()
        if ans:
            backup_snippet_file()
            print("Update backup file.")
    else:
        backup_snippet_file()
        print("Created backup file `{}`.".format(BACKUP_FILE))


def backup_snippet_file():
    """Copy `python.json` into `python_backup.json`.
    """
    src_filepath = get_vscode_snippet_filepath(SNIPPET_FILE)
    dist_filepath = get_vscode_snippet_filepath(BACKUP_FILE)
    shutil.copy(src_filepath, dist_filepath)


def write_snippets_in_vscode_file(snippet_dict):
    """Write snippet into vscode setting file.
    """
    python_snippet_file = get_vscode_snippet_filepath(SNIPPET_FILE)
    with open(python_snippet_file, 'w') as f:
        json.dump(snippet_dict, f, indent='\t')


def is_python_json_exists(filename):
    python_snippet_file = get_vscode_snippet_filepath(filename)
    if os.path.isfile(python_snippet_file):
        return True
    else:
        return False
