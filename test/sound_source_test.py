import unittest
from unknown import sound_source

MOCK_FILES = {
    'simple.wav': [
        [0x0000, 0x0000],
    ],
    'biramp.wav': [
        [0x0000, 0xFFFF],
        [0x4000, 0xAFFF],
        [0x8000, 0x7FFF],
        [0xB000, 0x3FFF],
    ],
}


class MockWave:
    def __init__(self, name):
        as_bytes = []
        for l, r in MOCK_FILES[name]:
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


def SoundSource(name, fade_frames=0):
    return sound_source.SoundSource(name, fade_frames, MockWave)


class ImportAllTest(unittest.TestCase):
    def test_simple(self):
        source = SoundSource('simple.wav')
        self.assertEqual(source.next_frame(), (0x0000, 0x0000))
        self.assertFalse(source.next_frame())
