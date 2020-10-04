import fire
from .pysnitlib.snippetcollector import register_snippets
from .pysnitlib.vscode import show_registered_snippets
from .pysnitlib import snippetfileio as snptio


class Commands:

    @staticmethod
    def help():
        """show help messages
        """
        pass

    @staticmethod
    def backup():
        """
        """
        snptio.backup()

    @staticmethod
    def restore():
        """Restore 'python.json' from 'python_backup.json`.
        """
        snptio.restore()

    @staticmethod
    def snpt(file='snippet.toml'):
        """Register snippets from snippet setting file.
        :param filepath: file path of snippet setting file. default value is `./snippet.toml`
        """
        snptio.backup()
        snippet_dict = register_snippets(file)
        snptio.write_snippets_in_vscode_file(snippet_dict)

    @staticmethod
    def list():
        """Show all snippets registered now.
        """
        show_registered_snippets()


def main():
    fire.Fire(Commands)


if __name__ == '__main__':
    main()
