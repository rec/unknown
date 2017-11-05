import os

SUFFIXES = '.aif', '.aiff', '.flac', '.mp3', '.wav'


def get_files(root='samples', verbose=False):
    for dirpath, dirnames, filenames in os.walk(os.path.abspath(root)):
        for file in filenames:
            if any(file.endswith(s) for s in SUFFIXES):
                yield os.path.join(dirpath, file)
            elif verbose:
                print('Skipped file', file)


if __name__ == '__main__':
    print(*get_files(verbose=True), sep='\n')
