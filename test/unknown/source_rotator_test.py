import unittest
from unknown import source_rotator
from . import mocks


class MockOutput:
    results = []

    def writeframes(self, frame):
        self.results += [frame]


class RotateSourcesTest(unittest.TestCase):
    def test_rotate_dc(self):
        in1 = mocks.combine(3, 'dc.wav', 'dc.wav')
        in2 = mocks.combine(3, 'dc.wav', 'dc.wav')
        outs = MockOutput(), MockOutput(), MockOutput()
        speed = 2 * source_rotator.FRAMES_PER_MINUTE
        source_rotator.source_rotator((in1, in2), outs, speed)
