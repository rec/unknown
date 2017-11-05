import json, os, sys

SUFFIXES = '.aif', '.aiff', '.flac', '.mp3', '.wav'


def get_files(root='samples', verbose=False):
    for dirpath, dirnames, filenames in os.walk(os.path.abspath(root)):
        for file in filenames:
            if any(file.endswith(s) for s in SUFFIXES):
                yield os.path.join(dirpath, file)
            elif verbose:
                print('Skipped file', file)


def get_files_by_category(root='samples', verbose=False):
    result = {'berlin': [], 'africa': []}
    for f in get_files(root, verbose):
        result['berlin' if '/berlin/' in f else 'africa'].append(f)
    return result



if __name__ == '__main__':
    json.dump(get_files_by_category(), sys.stdout, indent=2)
