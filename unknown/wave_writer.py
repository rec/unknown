import wave
from . import constants


class WaveWriter:
    def __init__(self, filename):
        self.fp = wave.open(filename, 'wb')
        self.fp.setnchannels(constants.NCHANNELS_OUT)
        self.fp.setsampwidth(constants.SAMPWIDTH)
        self.fp.setframerate(constants.FRAMERATE)
        self.frame = bytearray(constants.SAMPWIDTH)

    def writeframe(self, left, right):
        self.frame[:] = left, right
        self.fp.writeframes(self.frame)
