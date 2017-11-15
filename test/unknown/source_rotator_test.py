import unittest
from unknown import source_rotator
from . import mocks


class MockOutput:
    def __init__(self):
        self.results = []

    def writeframes(self, frame):
        self.results.append(frame)


class RotateSourcesTest(unittest.TestCase):
    def compare(self, expected, actual):
        expected = list(expected)
        actual = [a + 256 * b for a, b in actual]
        le, la = len(expected), len(actual)
        if le != la:
            print('Lengths differ: expected =', le, ' actual =', la)
        if expected != actual:
            print('compare FAILED')
            print(*['        0x%04x,' % a for a in actual], sep='\n')
        self.assertEqual(expected, actual)

    def combine_compare(self, files, fade, speed, expected):
        ins = [mocks.combine(fade, f, f) for f in files]
        outs = MockOutput(), MockOutput(), MockOutput(), MockOutput()
        speed *= source_rotator.FRAMES_PER_MINUTE
        source_rotator.source_rotator(ins, outs, speed)
        for expected_actual in zip(expected, (o.results for o in outs)):
            self.compare(*expected_actual)
        self.assertEqual(len(expected), 4)

    def test_rotate_dc(self):
        files = ['dc2.wav', 'dc2.wav']
        self.combine_compare(files, 0, 0, ROTATE_DC)
        self.combine_compare(files, 0, 1 / 4, ROTATE_DC)
        self.combine_compare(files, 0, 1 / 3, ROTATE_DC)
        self.combine_compare(files, 0, 1, ROTATE_DC)
        self.combine_compare(files, 0, 3, ROTATE_DC)
        self.combine_compare(files, 0, 4, ROTATE_DC)

    def test_fade_dc2(self):
        files = ['dc2.wav', 'dc2.wav']
        self.combine_compare(files, 2, 0, FADE_DC2)
        self.combine_compare(files, 2, 1 / 4, FADE_DC2)
        self.combine_compare(files, 2, 1 / 3, FADE_DC2)
        self.combine_compare(files, 2, 1, FADE_DC2)
        self.combine_compare(files, 2, 3, FADE_DC2)
        self.combine_compare(files, 2, 4, FADE_DC2)

    def test_fade_dc3(self):
        files = ['dc2.wav', 'dc2.wav']
        self.combine_compare(files, 3, 0, FADE_DC3)
        self.combine_compare(files, 2, 1 / 4, FADE_DC2)
        self.combine_compare(files, 2, 1 / 3, FADE_DC2)
        self.combine_compare(files, 2, 1, FADE_DC2)
        self.combine_compare(files, 2, 3, FADE_DC2)
        self.combine_compare(files, 2, 4, FADE_DC2)

    def test_rotate_saw(self):
        files = ['saw.wav', 'saw.wav']
        self.combine_compare(files, 0, 0, ROTATE_SAW)


ROTATE_SAW = (
    (0x0000, 0x0880, 0x1100, 0x1980, 0x0000, 0x0880, 0x1100, 0x1980),
    (0x0000, 0x0880, 0x1100, 0x1980, 0x0000, 0x0880, 0x1100, 0x1980),
    (0x0000, 0x0880, 0x1100, 0x1980, 0x0000, 0x0880, 0x1100, 0x1980),
    (0x0000, 0x0880, 0x1100, 0x1980, 0x0000, 0x0880, 0x1100, 0x1980),
)

ROTATE_DC = (
    (0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000),
    (0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000),
    (0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000),
    (0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000, 0x1000),
)

FADE_DC2 = (
    (0x0000, 0x0800, 0x1000, 0x1000, 0x1000, 0x0800),
    (0x0000, 0x0800, 0x1000, 0x1000, 0x1000, 0x0800),
    (0x0000, 0x0800, 0x1000, 0x1000, 0x1000, 0x0800),
    (0x0000, 0x0800, 0x1000, 0x1000, 0x1000, 0x0800),
)

FADE_DC3 = (
    (0x0000, 0x0555, 0x1000, 0x1000, 0x0555),
    (0x0000, 0x0555, 0x1000, 0x1000, 0x0555),
    (0x0000, 0x0555, 0x1000, 0x1000, 0x0555),
    (0x0000, 0x0555, 0x1000, 0x1000, 0x0555),
)
