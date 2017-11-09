import numpy
from . import constants, rotations

FRAMES_PER_MINUTE = 60 * constants.FRAME_RATE


def rotate_sources(ins, outs, speeds, in_rotations=None, out_rotations=None):
    """
    rotation units are 1.0 == 360 degrees
    Arguments:
      speeds -- rotation speed in rotations per minute (rpms).
          speeds can either be a single value in which case it's the same for
          all ins, or a list that is the same length as the number of ins.
          negative speeds ("counterclockwise") are also possible.

    """
    in_rotations = in_rotations or [i / len(ins) for i in range(len(ins))]
    out_rotations = out_rotations or [i / len(outs) for i in range(len(outs))]
    out_rotations = rotations.Rotations(out_rotations)

    # Convert speeds from rpms to rotations per frame
    try:
        speeds = tuple(s / FRAMES_PER_MINUTE for s in speeds)
    except TypeError:
        speeds = tuple(speeds / FRAMES_PER_MINUTE for i in ins)

    out_frames = numpy.zeros((len(outs), 2))

    for frame_index, frames in enumerate(zip(*ins)):
        out_frames.fill(0)
        for frame, speed, rotation in zip(frames, speeds, in_rotations):
            frame = numpy.array(frame)
            index, ratio = out_rotations.find(rotation + frame_index * speed)
            out_frames[index] = ratio  # WRONG
