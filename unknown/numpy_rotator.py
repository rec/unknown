import numpy as np
import math, wavio
from . import constants

FRAMERATE = constants.FRAMERATE


class Outputs:
    def __init__(self, in, outs, speeds, in_rotations, out_rotations, spread,
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
        self.samples = numpy.zeros((len(outs), self.length), dtype=dtype)

        self.fade_in = self.linspace(0, 1, fade)
        self.fade_out = self.linspace(1, 0, fade)

    def run(self):
        for files, speed, in_rotation in self.ins:
            frames = 0
            rotation = self.make_rotation(speed, in_rotation)
            for file in self.in_files:
                frames = self.apply_file(file, rotation, frames)

        for samples in self.samples():
            self.fade_samples(samples)

        for file, samples in zip(self.outs, self.samples):
            print('Writing', out, '....', end='')
            wave = wavio.write(file, data, FRAMERATE, scale='none', sampwidth=2)
            print(' done')

    def fade_samples(self, samples):
        samples[0 : self.fade] *= self.fade_in
        samples[-self.fade : ] *= self.fade_out

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



class Rotator:
    def __init__(self, outputs, speed, in_rotation):
        self.outputs = outputs
        self.in_rotation = in_rotation
        self.frames = 0

        # Now compute the rotation curve.
        segment_count = 1 + len(outputs.samples)
        segment = round(1 / (speed * segment_count))

        curve = np.zeros(segment_count * segment, dtype=outputs.dtype)

        curve[:segment] = self.linspace(0, 1, segment)
        curve[segment:2 * segment] = self.linspace(1, 0, segment)

        copy_count = 1 + math.floor(outputs.samples.shape[1] / len(curve))
        self.rotation = self.np.tile(curve, copy_count)


def rotator(ins, outs, speeds, in_rotations, out_rotations, spread,
            gap=0, length=60 * 60, fade=4, dtype='float'):
    """
    These names are legacy.

    speeds is how fast each input rotates in "rotations per frame"
    which will generally be a small non-negative number as a frame
    is a very small time interval!

    ins is a list of lists of files.
    out is a list of files.

    in_rotations are fixed rotation offsets for each input's
    out_rotations is not used in this implementation.

    spread is the rotation offset for each samples, left or right,
    against the middle

    """
    assert len(ins) == len(speeds)

    gap_frames = gap * FRAMERATE
    fade_frames = fade * FRAMERATE

    outputs = Outputs(outs, length * FRAMERATE, fade * FRAMERATE)

    for in_files, speed, in_rotation in zip(ins, speeds, in_rotations):
        rotator = Rotator(outputs, speed)
        for file in in_files:
            rotator.apply_file(file, spread, in_rotation, out_rotations, gap)

    outputs.fade_samples()
    outputs.write()
