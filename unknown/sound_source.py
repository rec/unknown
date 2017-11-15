import wave
from . import constants


class SoundSource:
    def __init__(self, file, fade_frames, wave_open=None):
        self.byte_index = 0
        with (wave_open or wave.open)(file) as fp:
            self.frames = fp.readframes(fp.getnframes())
        self.fade_in_bytes = fade_frames * constants.FRAME_SIZE_IN
        self.fade_out_bytes = len(self.frames) - self.fade_in_bytes

    def in_fade_out(self):
        return self.byte_index >= self.fade_out_bytes

    def in_fade_in(self):
        return self.byte_index < self.fade_in_bytes

    def __iter__(self):
        return self

    def __str__(self):
        return 'byte_index = %s(%s), in = %s, out = %s' % (
            self.byte_index, len(self.frames), self.fade_in_bytes,
            self.fade_out_bytes)

    def __next__(self):
        if self.byte_index >= len(self.frames):
            raise StopIteration

        if self.in_fade_in():
            fade = self.byte_index / self.fade_in_bytes
        elif self.in_fade_out():
            remaining = len(self.frames) - self.byte_index
            fade = remaining / self.fade_in_bytes
        else:
            fade = 1

        llo, lhi, rlo, rhi = self.frames[self.byte_index:self.byte_index + 4]
        left, right = 256 * lhi + llo, 256 * rhi + rlo

        self.byte_index += 4
        return round(left * fade), round(right * fade)
