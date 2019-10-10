import sys

def warning(str):
    print("WARNING: ", str, file=sys.stderr)

def error(str):
    print("ERROR: ", str, file=sys.stderr)
