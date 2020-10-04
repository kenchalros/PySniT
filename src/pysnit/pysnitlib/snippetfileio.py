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
    if not _is_python_json_exists(SNIPPET_FILE):
        print("`{}` to back up doesn't exist.".format(SNIPPET_FILE))
        return

    if _is_python_json_exists(BACKUP_FILE):
        print("`{}` already exists.".format(BACKUP_FILE))
        print("Update backup file?")
        ans = yes_or_no()
        if ans:
            _copy_file(SNIPPET_FILE, BACKUP_FILE)
            print("Update backup file.")
    else:
        _copy_file(SNIPPET_FILE, BACKUP_FILE)
        print("Created backup file `{}`.".format(BACKUP_FILE))


def restore():
    """Restore 'python.json' from 'python_backup.json'.
    """
    if not _is_python_json_exists(BACKUP_FILE):
        print("'{}' to restore doesn't exists.".format(BACKUP_FILE))
        return
    _copy_file(BACKUP_FILE, SNIPPET_FILE)
    print("Restore snippet file.")


def _copy_file(srcfile, distfile):
    src_filepath = get_vscode_snippet_filepath(srcfile)
    dist_filepath = get_vscode_snippet_filepath(distfile)
    shutil.copy(src_filepath, dist_filepath)


def write_snippets_in_vscode_file(snippet_dict):
    """Write snippet into vscode setting file.
    """
    python_snippet_file = get_vscode_snippet_filepath(SNIPPET_FILE)
    with open(python_snippet_file, 'w') as f:
        json.dump(snippet_dict, f, indent='\t')


def _is_python_json_exists(filename) -> bool:
    """If a file with the filename exists, return True, otherwise False.
    :param filename
    :param file exsitance
    """
    python_snippet_file = get_vscode_snippet_filepath(filename)
    return os.path.isfile(python_snippet_file)
