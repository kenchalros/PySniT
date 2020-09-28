from functools import reduce


def f_chain(chain_initializer, *funcs):
    """Chain functions.
    :param chain_initializer: target to apply functions.
    :param funcs: functions to apply.
    :return result of applying to initializer.

    ### example
    ```python
    f_chain(2,
            lambda x:x*2,
            lambda x:x+1)
    # => 5

    f_chain([1,2,3],
            lambda lst: [x*2 for x in lst],
            lambda lst: [x+1 for x in lst])
    # => [3,5,7]
    ```
    """
    return reduce(lambda x, f: f(x), funcs, chain_initializer)
