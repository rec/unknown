from . import combine_sources, constants, rotations, wave_writer

FRAMES_PER_MINUTE = 60 * constants.FRAMERATE


def _python_rotator(ins, outs, speeds, in_rotations, out_rotations, spread):
    ins = [combine_sources.CombineSources(*i) for i in ins]

    print('opening outputs')
    outs = [wave_writer.WaveWriter(o) for o in outs]

    for frame_index, frames in enumerate(zip(*ins)):
        out_frames = [0] * len(outs)

        for frame, speed, rotation in zip(frames, speeds, in_rotations):
            left, right = frame
            rotation += frame_index * speed

            for channel, offset in (left, -spread), (right, spread):
                index, ratio = out_rotations.find(rotation + offset)
                out_frames[index] += ratio * channel
                out_frames[index + 1] += (1 - ratio) * channel

        for sample, out in zip(out_frames, outs):
            round_sample = min(round(sample), 65535)
            high, low = divmod(round_sample, 256)
            out.writeframe(low, high)


def source_rotator(
        ins, outs, rotator=None, speeds=constants.DEFAULT_ROTATION_SPEED,
        in_rotations=None, out_rotations=None, stereo_spread=None):
    """
    rotations have 1.0 meaning a full rotation (360 degrees)

    Arguments:
      speeds -- rotation speed in rotations per minute (rpms).
          speeds can either be a single value in which case it's the same for
          all ins, or a list that is the same length as the number of ins.
          negative speeds ("counterclockwise") are also possible.

    """
    in_rotations = in_rotations or [i / len(ins) for i in range(len(ins))]
    out_rotations = out_rotations or [i / len(outs) for i in range(len(outs))]
    out_rotations = rotations.Rotations(out_rotations)

    if stereo_spread is None:
        stereo_spread = 1 / len(outs)
    spread = stereo_spread / 2

    # Convert speeds from rpms to rotations per frame
    try:
        speeds = [s / FRAMES_PER_MINUTE for s in speeds]
    except TypeError:
        speeds = [speeds / FRAMES_PER_MINUTE for i in ins]

    (rotator or _python_rotator)(
        ins, outs, speeds, in_rotations, out_rotations, spread)
