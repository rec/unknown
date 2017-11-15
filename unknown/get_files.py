import os
from . import util

SUFFIXES = '.aif', '.aiff', '.flac', '.mp3', '.wav'


def is_audio_file(file):
    return any(file.endswith(s) for s in SUFFIXES)


def normalize(f):
    return os.path.abspath(os.path.expanduser(f))


def get_files(root='samples', verbose=False):
    for dirpath, dirnames, filenames in os.walk(normalize(root)):
        for file in filenames:
            if is_audio_file(file):
                yield os.path.join(dirpath, file)
            elif verbose:
                print('Skipped file', file)


def get_all_files(files):
    for file in files:
        file = normalize(file)
        if is_audio_file(file):
            yield file
        elif os.path.isdir(file):
            for f in get_files(file):
                yield f


def get_files_by_category(root='samples', verbose=False):
    result = {'berlin': [], 'africa': []}
    for f in get_files(root, verbose):
        result['berlin' if '/berlin/' in f else 'africa'].append(f)
    return result


if __name__ == '__main__':
    util.json_dump(get_files_by_category())
