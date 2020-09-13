from inspect import getsource, getdoc

class snippet:
    funcs = []
    def __init__(self, func):
        self.code = self.src_to_code(func)
        self.__class__.funcs.append(self.code)

    @staticmethod
    def getsource(src):
        return getsource(src)

    def __call__(self):
        self.__class__.funcs.append(self.code)
        print('Hello Decorator!')
