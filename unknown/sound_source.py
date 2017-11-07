import wave

NCHANNELS = 2
SAMPWIDTH = 2
FRAMESIZE = NCHANNELS * SAMPWIDTH
FRAMERATE = 48000


def open_wave_for_write(filename):
    fp = wave.open(filename, 'wb')
    fp.setnchannels(NCHANNELS)
    fp.setsampwidth(SAMPWIDTH)
    fp.setframerate(FRAMERATE)
    return fp


class SoundSource:
    def __init__(self, file, fade_frames):
        self.byte_index = 0
        with wave.open(file) as fp:
            self.frames = fp.readframes(fp.nframes())
        self.fade_in_bytes = fade_frames * FRAME_SIZE
        self.fade_out_bytes = len(frames) - self.fade_in_bytes

    def in_fade_out(self):
        return self.byte_index >= self.fade_out_bytes

    def in_fade_in(self):
        return self.byte_index < self.fade_in_bytes

    def next_frame(self):
        if self.byte_index >= len(self.frames):
            return

        if self.in_fade_in():
            fade = self.byte_index / self.fade_in_bytes
        elif self.in_fade_out():
            fade = (len(frames) - self.byte_index) / self.fade_in_bytes
        else:
            fade = 1

        llo, lhi, rlo, rhi = self.frames[self.byte_index:self.byte_index + 4]
        left, right = 256 * lhi + llo, 256 * rhi + rlo

        self.byte_index += 4
        return left * fade, right * fade
