import numpy as np
import json, math, os, sys, traceback, wave
from . import constants, files, file_durations

FRAMERATE = constants.FRAMERATE
MIN, MAX = -0x8000, 0x7fff
DEBUG = False


def rotate(ins, outs, speeds, in_rotations, out_rotations, spread, gap=0,
           length=0, fade=0, dtype='float', gain=None, rotation_period=10,
           combined=None, sox_combine=False, directory=''):
    def lengths():
        min_total_length, max_source_length = float('inf'), 0
        for in_files in ins:
            source_lengths = [files.framecount(f) for f in in_files]
            max_source_length = max(max_source_length, *source_lengths)

            total = (len(source_lengths) - 1) * gap + sum(source_lengths)
            min_total_length = min(min_total_length, total)

        return min_total_length, max_source_length

    def apply_fade(samples):
        if fade:
            samples[0:fade] *= fade_in
            samples[-fade:] *= fade_out
        return samples

    def linspace(start, stop, num):
        return np.linspace(start, stop, num, endpoint=False, dtype=dtype)

    def make_rotation(rotation_period):
        # Compute the rotation curve, a sawtooth-like thing.
        if rotation_period is None:
            rotation_frames = FRAMERATE / speeds[0]
        else:
            rotation_frames = rotation_period * FRAMERATE
        print(hex(int(rotation_frames)), rotation_frames)
        assert rotation_frames < 1000000000
        segment = round(rotation_frames / len(outs))
        curve = np.zeros(segment * len(outs), dtype=dtype)

        curve[:segment] = linspace(0, 1, segment)
        curve[segment:2 * segment] = linspace(1, 0, segment)

        # TODO: this is a huge overestimate
        copy_count = 2 + 2 * math.floor(max_source_length / len(curve))
        return len(curve), np.tile(curve, copy_count)

    def mix_one_input(in_files, in_rotation):
        frames = 0
        for file in in_files:
            if frames >= length:
                print('Skipping', short_filename(file))
                continue
            rotation = in_rotation + (frames / rotation_frames)
            print(format_time(frames, True), short_filename(file))
            try:
                state = 'open file'
                left, right = files.read(file)

                state = 'mix file'
                if right is None:
                    mix_channel(left, rotation, frames)
                else:
                    mix_channel(left, rotation - spread, frames)
                    mix_channel(right, rotation + spread, frames)

            except KeyboardInterrupt:
                raise
            except:
                print('ERROR: Failed to', state, file)
                traceback.print_exc()
                continue

            frames += len(left) + gap

    def mix_channel(channel, rotation, frames):
        apply_fade(channel)

        for out, out_rotation in zip(output_samples, out_rotations):
            rot = (rotation + out_rotation) % 1
            offset = round(rot * rotation_frames)
            remaining = len(out) - frames

            c = channel if (len(channel) <= remaining) else channel[:remaining]
            out[frames:frames + len(c)] += (
                c * rotation_curve[offset:offset + len(c)])

    def short_filename(file):
        short = 'africa' if '/africa/' in file else 'berlin'
        return os.path.join(short, os.path.basename(file))

    def format_time(frames, use_hours=False):
        return file_durations.format_time(frames / FRAMERATE, use_hours)

    def limit(ins, gain, samples):
        for s in samples:
            apply_fade(s)

        if True:
            return

        if not gain:
            gain = 1 / len(ins)

        if gain != 1:
            samples *= gain

        limit_gain = max(1, samples.min() / MIN, samples.max() / MAX)
        if limit_gain > 1:
            print('WARNING: sample overs', limit_gain)
            samples /= limit_gain

    out_rotations = out_rotations.rotations
    gap = round(FRAMERATE * gap)
    fade = round(FRAMERATE * fade)
    if directory and not directory.endswith('/'):
        directory += '/'

    assert len(ins) == len(in_rotations)
    assert len(outs) == len(out_rotations)

    total_length, max_source_length = lengths()
    length = round(FRAMERATE * length) if length else total_length

    output_samples = np.zeros((len(outs), length), dtype=dtype)
    rotation_frames, rotation_curve = make_rotation(rotation_period)

    print('Length of output', format_time(length, True))
    print('Rotation time', format_time(rotation_frames),
          format_time(1 / speeds[0]))

    if fade:
        fade_in = linspace(0, 1, fade)
        fade_out = linspace(1, 0, fade)

    for in_files, in_rotation in zip(ins, in_rotations):
        mix_one_input(in_files, in_rotation)

    limit(ins, gain, output_samples)

    for file, data in zip(outs, output_samples):
        files.write(directory + file, data)

    if combined:
        if sox_combine:
            files.sox_combine(directory + combined, outs)
        else:
            files.combine(directory + combined, output_samples)
