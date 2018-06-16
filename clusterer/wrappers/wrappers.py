from functools import wraps

def io_wrap(func):
    @wraps(func)
    def wrapped(*args,**kws):
        while True:
            if (not args[0].empty()):
                input = args[0].get()
                output = func(input)
                args[1].put(output)

    return wrapped

def i_wrap(func):
    @wraps(func)
    def wrapped(*args,**kws):
        while True:
            output = func()
            args[0].put(output)

    return wrapped

def o_wrap(func):
    @wraps(func)
    def wrapped(*args,**kws):
        while True:
            if (not args[0].empty()):
                input = args[0].get()
                func(input)

    return wrapped
