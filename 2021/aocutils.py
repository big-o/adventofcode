import inspect
import sys


def infer_input():
    day = inspect.stack()[-1].filename.split(".")[0][3:]
    return f"input/{day}"


def run(callback, args=None, kwargs=None, filename=None, stream=True):
    if not filename:
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        else:
            filename = infer_input()

    args = args or tuple()
    kwargs = kwargs or {}
    with open(filename) as fh:
        if stream:
            result = callback(fh, *args, **kwargs)
        else:
            result = callback([line.rstrip("\n") for line in fh], *args, **kwargs)

    print(result)
