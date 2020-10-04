import fire
from .pysnitlib.snippetcollector import register_snippets
from .pysnitlib.vscode import show_registered_snippets
from .pysnitlib import snippetfileio as snptio
from .pysnitlib.funcs import f_chain


class Commands:
    @staticmethod
    def backup():
        """Backup 'python.json' to 'python_backup.json'.
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
        f_chain(file,
                register_snippets,
                snptio.write_snippets_in_vscode_file)

    @staticmethod
    def list():
        """Show all snippets registered now.
        """
        show_registered_snippets()


def main():
    fire.Fire(Commands)


if __name__ == '__main__':
    main()
