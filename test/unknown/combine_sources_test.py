import unittest
from . import mocks


class CombineSourcesTest(unittest.TestCase):
    def run_test(self, expected, fade_frames, *files):
        mocks.compare(expected, mocks.combine(fade_frames, *files), self)

    def test_empty(self):
        self.run_test((), 0)
        self.run_test((), 3)

    def test_single(self):
        self.run_test(SINGLE, 0, 'biramp.wav')

    def test_single_with_fade(self):
        self.run_test(SINGLE_WITH_FADE, 3, 'biramp.wav')

    def test_double_without_fade(self):
        self.run_test(DOUBLE_WITHOUT_FADE, 0, 'biramp.wav', 'biramp.wav')

    def test_double_with_fade(self):
        self.run_test(DOUBLE_WITH_FADE, 3, 'biramp.wav', 'biramp.wav')

    def test_combine_without_fade(self):
        self.run_test(COMBINE_WITHOUT_FADE, 0,
                      'biramp.wav', 'biramp.wav', 'biramp2.wav')

    def test_combine_with_fade(self):
        self.run_test(COMBINE_WITH_FADE, 3,
                      'biramp.wav', 'biramp.wav', 'biramp2.wav')

    def test_dc_without_fade(self):
        self.run_test(DC_WITHOUT_FADE, 0, 'dc.wav', 'dc.wav', 'dc.wav')

    def test_dc_with_fade(self):
        self.run_test(DC_WITH_FADE, 3, 'dc.wav', 'dc.wav', 'dc.wav')


SINGLE = (
    (0x0000, 0xffff),
    (0x1000, 0xefff),
    (0x2000, 0xdfff),
    (0x3000, 0xcfff),
    (0x4000, 0xbfff),
    (0x5000, 0xafff),
    (0x6000, 0x9fff),
    (0x7000, 0x8fff),
    (0x8000, 0x7fff),
)

SINGLE_WITH_FADE = (
    (0x0000, 0x0000),
    (0x0555, 0x5000),
    (0x1555, 0x9555),
    (0x3000, 0xcfff),
    (0x4000, 0xbfff),
    (0x5000, 0xafff),
    (0x6000, 0x9fff),
    (0x4aab, 0x5fff),
    (0x2aab, 0x2aaa),
)

DOUBLE_WITHOUT_FADE = (
    (0x0000, 0xffff),
    (0x1000, 0xefff),
    (0x2000, 0xdfff),
    (0x3000, 0xcfff),
    (0x4000, 0xbfff),
    (0x5000, 0xafff),
    (0x6000, 0x9fff),
    (0x7000, 0x8fff),
    (0x8000, 0x7fff),
    (0x0000, 0xffff),
    (0x1000, 0xefff),
    (0x2000, 0xdfff),
    (0x3000, 0xcfff),
    (0x4000, 0xbfff),
    (0x5000, 0xafff),
    (0x6000, 0x9fff),
    (0x7000, 0x8fff),
    (0x8000, 0x7fff),
)
DOUBLE_WITH_FADE = (
    (0x0000, 0x0000),
    (0x0555, 0x5000),
    (0x1555, 0x9555),
    (0x3000, 0xcfff),
    (0x4000, 0xbfff),
    (0x5000, 0xafff),
    (0x6000, 0x9fff),
    (0x5000, 0xafff),
    (0x4000, 0xbfff),
    (0x3000, 0xcfff),
    (0x4000, 0xbfff),
    (0x5000, 0xafff),
    (0x6000, 0x9fff),
    (0x4aab, 0x5fff),
    (0x2aab, 0x2aaa),
)

COMBINE_WITHOUT_FADE = (
    (0x0000, 0xffff),
    (0x1000, 0xefff),
    (0x2000, 0xdfff),
    (0x3000, 0xcfff),
    (0x4000, 0xbfff),
    (0x5000, 0xafff),
    (0x6000, 0x9fff),
    (0x7000, 0x8fff),
    (0x8000, 0x7fff),
    (0x0000, 0xffff),
    (0x1000, 0xefff),
    (0x2000, 0xdfff),
    (0x3000, 0xcfff),
    (0x4000, 0xbfff),
    (0x5000, 0xafff),
    (0x6000, 0x9fff),
    (0x7000, 0x8fff),
    (0x8000, 0x7fff),
    (0x8000, 0x7fff),
    (0x7000, 0x8fff),
    (0x6000, 0x9fff),
    (0x5000, 0xafff),
    (0x4000, 0xbfff),
    (0x4000, 0xbfff),
    (0x4000, 0xbfff),
    (0x4000, 0xbfff),
    (0x3000, 0xcfff),
    (0x2000, 0xdfff),
    (0x1000, 0xefff),
    (0x0000, 0xffff),
)

COMBINE_WITH_FADE = (
    (0x0000, 0x0000),
    (0x0555, 0x5000),
    (0x1555, 0x9555),
    (0x3000, 0xcfff),
    (0x4000, 0xbfff),
    (0x5000, 0xafff),
    (0x6000, 0x9fff),
    (0x5000, 0xafff),
    (0x4000, 0xbfff),
    (0x3000, 0xcfff),
    (0x4000, 0xbfff),
    (0x5000, 0xafff),
    (0x6000, 0x9fff),
    (0x7000, 0x8fff),
    (0x6aab, 0x9554),
    (0x5000, 0xafff),
    (0x4000, 0xbfff),
    (0x4000, 0xbfff),
    (0x4000, 0xbfff),
    (0x4000, 0xbfff),
    (0x3000, 0xcfff),
    (0x2000, 0xdfff),
    (0x0aab, 0x9fff),
    (0x0000, 0x5555),
)

DC_WITHOUT_FADE = ((0x5000, 0x5000),) * 24

DC_WITH_FADE = (
    (0x0000, 0x0000),
    (0x1aab, 0x1aab),
    (0x3555, 0x3555),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x5000, 0x5000),
    (0x3555, 0x3555),
    (0x1aab, 0x1aab),
)
