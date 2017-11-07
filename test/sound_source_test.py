import unittest
from unknown import sound_source


class MockWave:
    MOCK_FILES = {
        'simple.wav': (
            (0x0000, 0x0000),
        ),
        'biramp.wav': (
            (0x0000, 0xFFFF),
            (0x1000, 0xEFFF),
            (0x2000, 0xDFFF),
            (0x3000, 0xCFFF),
            (0x4000, 0xBFFF),
            (0x5000, 0xAFFF),
            (0x6000, 0x9FFF),
            (0x7000, 0x8FFF),
            (0x8000, 0x7FFF),
        ),
    }

    def __init__(self, name):
        as_bytes = []
        for l, r in self.MOCK_FILES[name]:
            as_bytes.extend(reversed(divmod(r, 256) + divmod(r, 256)))
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
        self.assertEqual(list(expected), actual)

    def test_simple(self):
        self.assert_frames('simple.wav', (0x0000, 0x0000))
