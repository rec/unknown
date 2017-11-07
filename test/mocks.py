FILES = {
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

    'biramp2.wav': (
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
    ),
}


class MockWave:
    def __init__(self, name):
        as_bytes = []
        for l, r in FILES[name]:
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
