import json, sys
from . import constants, get_files, numpy_rotator, source_rotator


def rotate_score(ins, outs, fade=constants.DEFAULT_FADE_TIME,
                 use_numpy=True, **kwds):
    """
    Arguments:
    ins -- a list of lists of files or directories.
    outs -- either a base filename or a list of files.
    kwds -- are passed to source_rotator
    """
    print('rotate_score', kwds)
    print('ins', ins)
    print('outs', outs)
    print('fade', fade)

    if not use_numpy:
        fade /= constants.FRAMERATE

    ins = [[i] if isinstance(i, str) else i for i in ins]
    print('Finding files')
    ins = [list(get_files.get_all_files(i)) for i in ins]
    print('Input file counts are', *[len(i) for i in ins])

    outs = [get_files.normalize(o) for o in outs]
    rotator = use_numpy and numpy_rotator.rotate
    source_rotator.source_rotator(ins, outs, rotator, fade, **kwds)


def rotate_score_file(filename='score.json'):
    print('rotate_score_file', filename)
    rotate_score(**json.load(open(filename)))


if __name__ == '__main__':
    rotate_score_file(*sys.argv[1:])
