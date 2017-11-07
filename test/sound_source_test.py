import unittest
from unknown import sound_source

MOCK_FILES = {
    'simple.wav': (
        (0x0000, 0x0000),
    ),
    'biramp.wav': (
        (0x0000, 0xffff),
        (0x1000, 0xefff),
        (0x2000, 0xdfff),
        (0x3000, 0xcfff),
        (0x4000, 0xbfff),
        (0x5000, 0xafff),
        (0x6000, 0x9fff),
        (0x7000, 0x8fff),
        (0x8000, 0x7fff),
    ),
}


class MockWave:
    def __init__(self, name):
        as_bytes = []
        for l, r in MOCK_FILES[name]:
            as_bytes.extend(reversed(divmod(r, 256) + divmod(l, 256)))
        self.frames = bytes(as_bytes)

    def readframes(self, _):
        return self.frames

    def nframes(self):
        return len(self.frames) / 4

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class SoundSourceTest(unittest.TestCase):
    def assert_frames(self, name, *expected, fade_frames=0):
        source = sound_source.SoundSource(name, fade_frames, MockWave)
        actual = []
        while True:
            frame = source.next_frame()
            if not frame:
                break
            actual.append(frame)
        if list(expected) != actual:
            for a in actual:
                print('(0x%04x, 0x%04x),' % a)
        self.assertEqual(list(expected), actual)

    def test_simple(self):
        self.assert_frames('simple.wav', *MOCK_FILES['simple.wav'])

    def test_biramp(self):
        self.assert_frames('biramp.wav', *MOCK_FILES['biramp.wav'])

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
