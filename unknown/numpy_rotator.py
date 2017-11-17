import numpy as np
import math, wavio, wave
from . import constants

FRAMERATE = constants.FRAMERATE


def total_frames(files):
    return [wave.open(f).getnframes() for f in files]


class Rotator:
    def __init__(self, ins, outs, speeds, in_rotations, out_rotations, spread,
                 gap=0, length=None, fade=4, dtype='float'):
        assert len(ins) == len(speeds) == len(in_rotations)
        if length:
            self.length = length * FRAMERATE
        else:
            in_frames = [total_frames(i) for i in ins]
            self.length = min((len(i) - 1) * gap + sum(i) for i in in_frames)
        print('length =', int(self.length / FRAMERATE))
        self.ins = zip(ins, speeds, in_rotations)
        self.outs = outs
        self.out_rotations = out_rotations
        self.spread = spread
        self.gap = gap * FRAMERATE
        self.dtype = dtype
        self.fade = fade * FRAMERATE

        self.samples = np.zeros((len(outs), self.length), dtype=dtype)

        self.fade_in = self.linspace(0, 1, self.fade)
        self.fade_out = self.linspace(1, 0, self.fade)

    def run(self):
        for files, speed, in_rotation in self.ins:
            frames = 0
            rotation = self.make_rotation(speed)
            for file in files:
                frames = self.apply_file(file, rotation, frames, in_rotation)

        for samples in self.samples():
            self.fade_samples(samples)

        for file, data in zip(self.outs, self.samples):
            print('Writing', file, '....', end='')
            wavio.write(file, data, FRAMERATE, scale='none', sampwidth=2)
            print(' done')

    def fade_samples(self, samples):
        samples[0:self.fade] *= self.fade_in
        samples[-self.fade:] *= self.fade_out

    def linspace(self, start, stop, num):
        return np.linspace(start, stop, num, endpoint=False, dtype=self.dtype)

    def accumulate(self, samples, rotation_curve, rotation):
        self.fade_samples(samples)

        # Rotate into the output samples.
        # DANGER - do I need out_rotations?
        for out in self.samples:
            offset = round((rotation % 1) * FRAMERATE)
            rotated = rotation_curve[offset:offset + len(samples)]
            out[self.frames:self.frames + len(samples)] += rotated

    def make_rotation(self, speed):
        # Now compute the rotation curve.
        segment_count = 1 + len(self.samples)
        segment = round(1 / (speed * segment_count))

        curve = np.zeros(segment_count * segment, dtype=self.dtype)

        curve[:segment] = self.linspace(0, 1, segment)
        curve[segment:2 * segment] = self.linspace(1, 0, segment)

        copy_count = 1 + math.floor(self.samples.shape[1] / len(curve))
        return np.tile(curve, copy_count)

    def apply_file(self, file, rotation, frames, in_rotation):
        print('Reading', file, '....', end='')
        wave = wavio.read(file)
        print(' done')

        assert wave.sampwidth == 2 and wave.rate == FRAMERATE

        left, right = wave.data[:, 0], wave.data[:, 1]
        left, right = left.astype(self.dtype), right.astype(self.dtype)
        for c, s in (left, -self.spread), (right, self.spread):
            self.accumulate(c, rotation, s + in_rotation)

        return frames + (len(left) + self.gap)


def rotate(*args, **kwds):
    Rotator(*args, **kwds).run()
