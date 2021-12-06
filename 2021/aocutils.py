import inspect
import sys


def infer_input():
    day = inspect.stack()[-1].filename.split(".")[0][3:]
    return f"input/{day}"


def run(callback, *args, **kwargs):
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = infer_input()

    with open(filename) as fh:
        result = callback(fh, *args, **kwargs)

    print(result)
