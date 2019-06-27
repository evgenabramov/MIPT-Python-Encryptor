import sys
from contextlib import contextmanager


@contextmanager
def get_stream(stream, mode):
    if stream == sys.stdin:
        file = sys.stdin
    elif stream == sys.stdout:
        file = sys.stdout
    else:
        file = open(stream, mode)
    yield file
    if stream == sys.stdout:
        file.write('\n')
    if stream != sys.stdin and stream != sys.stdout:
        file.close()
