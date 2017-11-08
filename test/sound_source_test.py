import unittest
from . import mocks
from unknown import sound_source


class SoundSourceTest(unittest.TestCase):
    def assert_frames(self, name, *expected, fade_frames=0):
        source = sound_source.SoundSource(name, fade_frames, mocks.MockWave)
        self.assertTrue(mocks.compare(expected, source))

    def test_simple(self):
        self.assert_frames('simple.wav', *mocks.FILES['simple.wav'])

    def test_biramp(self):
        self.assert_frames('biramp.wav', *mocks.FILES['biramp.wav'])

    def test_fade(self):
        self.assert_frames(
            'biramp.wav',
            (0x0000, 0x0000),
            (0x0555, 0x5000),
            (0x1555, 0x9555),
            (0x3000, 0xcfff),
            (0x4000, 0xbfff),
            (0x5000, 0xafff),
            (0x5800, 0x92aa),
            (0x4155, 0x53ff),
            (0x2000, 0x2000),
            fade_frames=3)
