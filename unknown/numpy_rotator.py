import numpy as np
import math, wavio, wave
from . import constants

FRAMERATE = constants.FRAMERATE


def rotate(ins, outs, speeds, in_rotations, out_rotations, spread, gap=0,
           length=0, fade=0, dtype='float'):
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

    def make_rotation(speed):
        # Compute the rotation curve, a sawtooth-like thing.
        segment_count = 1 + len(outs)
        segment = round(1 / (speed * segment_count))

        curve = np.zeros(segment_count * segment, dtype=dtype)

        curve[:segment] = linspace(0, 1, segment)
        curve[segment:2 * segment] = linspace(1, 0, segment)

        copy_count = 1 + math.floor(max_source_length / len(curve))
        return np.tile(curve, copy_count)

    def read_file(file):
        print('Reading', file, '....', end='')
        wave = wavio.read(file)
        print(' done')
        assert wave.sampwidth == 2 and wave.rate == FRAMERATE

        return [apply_fade(wave.data[:, i].astype(dtype)) for i in (0, 1)]

    def write_output(file, data):
        print('Writing', file, '....', end='')
        wavio.write(file, data, FRAMERATE, scale='none', sampwidth=2)
        print(' done')

    def mix_one_input(files, speed, in_rotation):
        frames = 0
        curve = make_rotation(speed)
        for file in files:
            left, right = read_file(file)
            for channel, cspread in (left, -spread), (right, spread):
                mix_channel(channel, cspread + in_rotation, frames, curve)

            frames += len(left) + gap

    def mix_channel(channel, rotation, frames, curve):
        for out, out_rotation in zip(output_samples, out_rotations):
            # This one line is the key calculation and I am a little insecure
            # about it.
            offset = round(((rotation - out_rotation) % 1) * FRAMERATE)
            out[frames:frames + len(channel)] += (
                curve[offset:offset + len(channel)] * channel)

    out_rotations = out_rotations.rotations

    assert len(ins) == len(speeds) == len(in_rotations)
    assert len(outs) == len(out_rotations)

    gap = round(FRAMERATE * gap)
    fade = round(FRAMERATE * fade)

    total_length, max_source_length = lengths()
    length = round(FRAMERATE * length) if length else total_length

    output_samples = np.zeros((len(outs), length), dtype=dtype)

    if fade:
        fade_in = linspace(0, 1, fade)
        fade_out = linspace(1, 0, fade)

    for files, speed, in_rotation in zip(ins, speeds, in_rotations):
        mix_one_input(files, speed, in_rotation)

    for s in output_samples:
        apply_fade(s)

    for file, data in zip(outs, output_samples):
        write_outputs(file, data)
