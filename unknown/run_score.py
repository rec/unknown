import wave, json, sys
from . import combine_sources, constants, get_files, source_rotator


def open_wave_for_write(filename):
    fp = wave.open(filename, 'wb')
    fp.setnchannels(constants.NCHANNELS_OUT)
    fp.setsampwidth(constants.SAMPWIDTH)
    fp.setframerate(constants.FRAMERATE)
    return fp


def rotate_score(ins, outs, fade=constants.DEFAULT_FADE_TIME, **kwds):
    """
    Arguments:
    ins -- a list of lists of files or directories.
    outs -- either a base filename or a list of files.
    kwds -- are passed to source_rotator
    """

    fade_frames = fade / constants.FRAMERATE

    ins = [[i] if isinstance(i, str) else i for i in ins]
    ins = [get_files.get_all_files(i) for i in ins]
    ins = [combine_sources.CombineSources(fade_frames, *i) for i in ins]

    outs = [get_files.normalize(o) for o in outs]
    outs = [open_wave_for_write(o) for o in outs]

    source_rotator.source_rotator(ins, outs, **kwds)


def rotate_score_file(filename='score.json'):
    rotate_score(**json.load(open(filename)))


if __name__ == '__main__':
    rotate_score_file(*sys.argv[1:])
