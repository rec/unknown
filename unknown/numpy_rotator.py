import numpy as np
import math, wavio
from . import constants

FRAMERATE = constants.FRAMERATE


class Rotator:
    def __init__(self, ins, outs, speeds, in_rotations, out_rotations, spread,
                 gap=0, length=60 * 60, fade=4, dtype='float'):
        assert len(ins) == len(speeds) == len(in_rotations)
        self.ins = zip(ins, speeds, in_rotations)
        self.outs = outs
        self.out_rotations = out_rotations
        self.spread = spread
        self.gap = gap * FRAMERATE
        self.dtype = dtype
        self.fade = fade * FRAMERATE

        self.length = length * FRAMERATE
        self.samples = np.zeros((len(outs), self.length), dtype=dtype)

        self.fade_in = self.linspace(0, 1, fade)
        self.fade_out = self.linspace(1, 0, fade)

    def run(self):
        for files, speed, in_rotation in self.ins:
            frames = 0
            rotation = self.make_rotation(speed, in_rotation)
            for file in files:
                frames = self.apply_file(file, rotation, frames)

        for samples in self.samples():
            self.fade_samples(samples)

        for file, data in zip(self.outs, self.samples):
            print('Writing', out, '....', end='')
            wave = wavio.write(
                file, data, FRAMERATE, scale='none', sampwidth=2)
            print(' done')

    def fade_samples(self, samples):
        samples[0:self.fade] *= self.fade_in
        samples[-self.fade:] *= self.fade_out

    def linspace(self, start, stop, num):
        return np.linspace(start, stop, num, endpoint=False, dtype=self.dtype)

    def accumulate(self, samples, rotation_curve, rotation_offset):
        self.fade_samples(samples)

        # Rotate into the output samples.
        for out, out_rotation in zip(self.samples, self.out_rotations):
            rotation = rotation_offset + out_rotation
            offset = (rotation % 1) * FRAMERATE
            rotated = rotation_curve[offset:offset + len(samples)]
            out[self.frames:self.frames + len(samples)] += rotated

    def make_rotation(self, speed, in_rotation):
        # Now compute the rotation curve.
        segment_count = 1 + len(self.samples)
        segment = round(1 / (speed * segment_count))

        curve = np.zeros(segment_count * segment, dtype=self.dtype)

        curve[:segment] = self.linspace(0, 1, segment)
        curve[segment:2 * segment] = self.linspace(1, 0, segment)

        copy_count = 1 + math.floor(self.samples.shape[1] / len(curve))
        return np.tile(curve, copy_count)

    def apply_file(self, filename, rotation, frames):
        print('Reading', file, '....', end='')
        wave = wavio.read(file)
        print(' done')

        assert wave.sampwidth == 2 and wave.rate == FRAMERATE

        left, right = wave.data[:, 0], wave.data[:, 1]
        for c, s in (left, -spread), (right, spread):
            self.accumulate(c, rotation.rotation, s + self.in_rotation)

        return frames + (len(left) + gap)


def rotate(*args, **kwds):
    Rotator(*args, **kwds).run()
