import numpy as np
import math, os, traceback, wavio, wave
from . import constants
from . import file_durations

FRAMERATE = constants.FRAMERATE
MIN, MAX = -0x8000, 0x7fff


def rotate(ins, outs, speeds, in_rotations, out_rotations, spread, gap=0,
           length=0, fade=0, dtype='float', scale=None):
    def lengths():
        min_total_length, max_source_length = float('inf'), 0
        for files in ins:
            source_lengths = [wave.open(f).getnframes() for f in files]
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

    def make_rotation(rotation_frames):
        # Compute the rotation curve, a sawtooth-like thing.
        segment = round(rotation_frames / len(outs))
        curve = np.zeros(segment * len(outs), dtype=dtype)

        curve[:segment] = linspace(0, 1, segment)
        curve[segment:2 * segment] = linspace(1, 0, segment)

        # TODO: this is a huge overestimate
        copy_count = 2 + 2 * math.floor(max_source_length / len(curve))
        return len(curve), np.tile(curve, copy_count)

    def read_file(file):
        wave = wavio.read(file)
        assert wave.sampwidth == 2 and wave.rate == FRAMERATE

        return [apply_fade(wave.data[:, i].astype(dtype)) for i in (0, 1)]

    def write_output(file, data):
        print('Writing', file, '....')
        wavio.write(file, data, FRAMERATE, scale='none', sampwidth=2)

    def mix_one_input(files, in_rotation):
        frames = 0
        for file in files:
            if frames >= length:
                print('Skipping', short_filename(file))
                continue
            rotation = in_rotation + frames / rotation_frames
            print(format_time(frames, True), short_filename(file))
            try:
                state = 'open file'
                left, right = read_file(file)

                state = 'mix file'
                for channel, cspread in (left, -spread), (right, spread):
                    mix_channel(channel, cspread + rotation, frames)
            except KeyboardInterrupt:
                raise
            except:
                print('ERROR: Failed to', state, file)
                traceback.print_exc()
                continue

            frames += len(left) + gap

    def mix_channel(channel, rotation, frames):
        print('mix_channel', rotation, format_time(rotation_length))

        for out, out_rotation in zip(output_samples, out_rotations):
            rot = (rotation + out_rotation) % 1
            offset = round(rot * rotation_frames)
            remaining = len(out) - frames
            c = channel if (len(channel) <= remaining) else channel[:remaining]

            print('   ',
                  out_rotation, rot,
                  format_time(offset),
                  format_time(remaining),
                  format_time(len(c)),
                  format_time(frames),
                  )

            out[frames:frames + len(c)] += (
                c * rotation_curve[offset:offset + len(c)])

    def short_filename(file):
        short = 'africa' if '/africa/' in file else 'berlin'
        return os.path.join(short, os.path.basename(file))

    def format_time(frames, use_hours=False):
        return file_durations.format_time(frames / FRAMERATE, use_hours)

    def limit(ins, scale, samples):
        for s in samples:
            apply_fade(s)

        if not scale:
            scale = 1 / len(ins)

        if scale != 1:
            samples *= scale

        limit_scale = max(1, samples.min() / MIN, samples.max() / MAX)
        if limit_scale > 1:
            print('WARNING: sample overs', limit_scale)
            samples /= limit_scale

    # Simplify legacy arguments
    out_rotations = out_rotations.rotations
    gap = round(FRAMERATE * gap)
    fade = round(FRAMERATE * fade)

    assert len(ins) == len(in_rotations)
    assert len(outs) == len(out_rotations)

    total_length, max_source_length = lengths()
    length = round(FRAMERATE * length) if length else total_length

    print('Length of output', format_time(length, True))
    print('Max source time', format_time(max_source_length))

    output_samples = np.zeros((len(outs), length), dtype=dtype)
    rotation_frames, rotation_curve = make_rotation(1 / speeds[0])

    if fade:
        fade_in = linspace(0, 1, fade)
        fade_out = linspace(1, 0, fade)

    for files, in_rotation in zip(ins, in_rotations):
        mix_one_input(files, in_rotation)

    limit(ins, scale, output_samples)

    for file, data in zip(outs, output_samples):
        write_output(file, data)
