import json, sys


def json_dump(x):
    json.dump(x, sys.stdout, indent=2)
