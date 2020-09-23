import os
import json


def get_vscode_snippet_dirpath() -> str:
    """Get a path of vscode snippet directory.
    :return vscode_snippet_dir: a path of vscode snippet directory
    """
    homedir = os.environ['HOME']
    vscode_snippet_dir = homedir + '/Library/Application Support/Code/User/snippets/'
    return vscode_snippet_dir


def show_registered_snippets() -> None:
    """Show snippets registered now.
    """
    vscode_snippet_dir = get_vscode_snippet_dirpath()
    snippet_path = vscode_snippet_dir + 'python.json'
    if not os.path.isfile(snippet_path):
        print('No snippet file exists.')
        return
    snippets = None
    with open(snippet_path, 'r') as f:
        snippets = json.loads(f.read())
    for name, content in snippets.items():
        section_bar = '-'*(len(name))
        print(section_bar)
        print('{}'.format(name))
        print(section_bar)
        print('[prefix]\n{}'.format(content['prefix']))
        print('[description]\n{}'.format(content.get('description')))
        print('[body]')
        if isinstance(content['body'], list):
            print('\n'.join(content['body']).replace('\t', '    '))
        else:
            print(content['body'])
        print()
