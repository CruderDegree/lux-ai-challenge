import sys
"""
eprint
Same as print, but writes output to stderr instead of stdout
"""
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)