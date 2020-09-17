from pysnit.pysnitlib.snippet import snippet

@snippet(prefix='sample1_1',
         description='This snippet prefix is `sample1_1.`')
def sample1_prefix_and_description():
    pass

@snippet(prefix='sample1_2')
def sample1_only_prefix():
    pass

@snippet(prefix='sample1_3')
def sample1_wrong_option():
    pass

@snippet
def no_snippet_option():
    pass

@snippet(prefix='SampleClass',
         description='This is sample class.')
class SampleClass:
    def __init__(self):
        pass

    def hello(self):
        print('hello')

    def hoge(self, x):
        print(x+1)
