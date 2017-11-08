import unittest
from . import mocks
from unknown import combine_sources


class CombineSourcesTest(unittest.TestCase):
    def test_empty(self):
        combined = combine_sources.CombineSources(
            wave_open=mocks.MockWave, fade_frames=0)
        mocks.compare((), combined, self)

    def test_single(self):
        combined = combine_sources.CombineSources(
            'biramp.wav', wave_open=mocks.MockWave, fade_frames=0)
        expected = (
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
        mocks.compare(expected, combined, self)

    def test_single_with_fade(self):
        combined = combine_sources.CombineSources(
            'biramp.wav', wave_open=mocks.MockWave, fade_frames=3)
        expected = (
            (0x0000, 0x0000),
            (0x0555, 0x5000),
            (0x1555, 0x9555),
            (0x3000, 0xcfff),
            (0x4000, 0xbfff),
            (0x5000, 0xafff),
            (0x5800, 0x92aa),
            (0x4155, 0x53ff),
            (0x2000, 0x2000),
        )
        mocks.compare(expected, combined, self)

    def test_double_without_fade(self):
        combined = combine_sources.CombineSources(
            'biramp.wav', 'biramp.wav',
            wave_open=mocks.MockWave, fade_frames=0)
        expected = (
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
        mocks.compare(expected, combined, self)

    def test_double_with_fade(self):
        combined = combine_sources.CombineSources(
            'biramp.wav', 'biramp.wav',
            wave_open=mocks.MockWave, fade_frames=3)
        expected = (
        )
        mocks.compare(expected, combined, self)

    def test_combine_without_fade(self):
        combined = combine_sources.CombineSources(
            'biramp.wav', 'biramp.wav', 'biramp2.wav',
            wave_open=mocks.MockWave, fade_frames=0)
        self.assertTrue(mocks.compare((), combined))

    def test_combine_with_fade(self):
        combined = combine_sources.CombineSources(
            'biramp.wav', 'biramp.wav', 'biramp2.wav',
            wave_open=mocks.MockWave)
        self.assertTrue(mocks.compare((), combined))
