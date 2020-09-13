import fire


class Commands:

    @staticmethod
    def hello():
        print('Hello, PySnit!')


def main():
    fire.Fire(Commands)


if __name__ == '__main__':
    main()
