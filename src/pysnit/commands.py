import fire
from .pysnitlib.snippetcollector import SnippetCollector


class Commands:

    @staticmethod
    def help():
        """show help messages
        """
        pass

    @staticmethod
    def snpt(file='snippet.toml'):
        """register snippets from snippet manage file.
        :param filepath: file path of snippet manager file. default value is `snippet.toml`
        """
        SC = SnippetCollector(file)
        SC.register_snippets()


def main():
    fire.Fire(Commands)


if __name__ == '__main__':
    main()
