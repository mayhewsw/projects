__author__ = 'stephen'

def myfunc(func):
    print(func)
    return func

@myfunc
def anotherfunc():
    return 45


class Test():
    """ This player chooses randonly from the different options.
    """

    def __init__(self):

        print(anotherfunc())

r = Test()
