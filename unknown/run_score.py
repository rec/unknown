import json, sys
from . import (
    combine_sources, constants, get_files, source_rotator, wave_writer)


def rotate_score(ins, outs, fade=constants.DEFAULT_FADE_TIME, **kwds):
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

    fade_frames = fade / constants.FRAMERATE

    ins = [[i] if isinstance(i, str) else i for i in ins]
    print('Finding files')
    ins = [list(get_files.get_all_files(i)) for i in ins]
    print('File counts are', *[len(i) for i in ins])

    ins = [combine_sources.CombineSources(fade_frames, *i) for i in ins]

    print('opening outputs')
    outs = [get_files.normalize(o) for o in outs]
    outs = [wave_writer.WaveWriter(o) for o in outs]

    print('rotating')
    source_rotator.source_rotator(ins, outs, **kwds)


def rotate_score_file(filename='score.json'):
    print('rotate_score_file', filename)
    rotate_score(**json.load(open(filename)))


if __name__ == '__main__':
    rotate_score_file(*sys.argv[1:])
