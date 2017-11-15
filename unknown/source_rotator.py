from . import constants, rotations

FRAMES_PER_MINUTE = 60 * constants.FRAMERATE


def source_rotator(
        ins, outs, speeds, in_rotations=None, out_rotations=None,
        left_right_offset=0.5):
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

    for frame_index, frames in enumerate(zip(*ins)):
        def pf(frame):
            return '(0x%04x, 0x%04x)' % frame

        print()
        print(frame_index)
        print('source_rotator frames', [pf(f) for f in frames])
        out_frames = [0] * len(outs)
        for frame, speed, rotation in zip(frames, speeds, in_rotations):
            left, right = frame
            rotation += frame_index * speed
            for channel, offset in (left, 0), (right, left_right_offset):
                index, ratio = out_rotations.find(rotation + offset)
                print('rotating', index, '%4.2f' % ratio,
                      hex(channel), '%5.3f' % rotation, offset)
                print('%5.3f' % (ratio * channel),
                      '%5.3f' % ((1 - ratio) * channel))
                out_frames[index] += ratio * channel
                out_frames[index + 1] += (1 - ratio) * channel

        for i, (sample, out) in enumerate(zip(out_frames, outs)):
            round_sample = min(round(sample), 65535)
            result = tuple(reversed(divmod(round_sample, 256)))
            print('source_rotator', i, hex(round_sample), result)
            out.writeframes(result)
