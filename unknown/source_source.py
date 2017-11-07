import wave

# If FADE_TIME is positive, then there is a fade between consecutive pairs of
# source files of that many seconds.
#
# If SPACING_TIME is positive, then the start of the next source file is
# delayed by that many seconds.  The default is 0
#
# For example, if FADE_TIME = 0 and SPACING_TIME = 0, then each sample is played
# right after the other with no pause.
#
# If FADE_TIME = 3 and SPACING_TIME = 0 then starting 3 seconds before the end
# of each file, the first sample fades out and the second one fades in.
#
# If FADE_TIME = 0 and SPACING_TIME = 3 then each sample is played
# right after the other with a three second pause pause.
#
# If FADE_TIME = 3 and SPACING_TIME = 3 then each sample fades to nothing
# in its last three seconds, and then the next sample fades in in 3 seconds.


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


class OneSoundSource:
    def __init__(self, file, fade_frames):
        self.byte_index = 0
        with wave.open(file) as fp:
            self.frames = fp.readframes(fp.nframes())
        self.fade_in_bytes = fade_frames * FRAME_SIZE
        self.fade_out_bytes = len(frames) - self.fade_in_bytes

    def finished(self):
        return self.byte_index < len(self.frames)

    def get_frame(self):
        b1 = self.byte_index
        b2 = b1 + FRAME_SIZE
        self.byte_index = b2
        l_lo, l_hi, r_lo, r_hi = self.frames[b1:b2]
        left, right = 256 * l_hi + l_lo, 256 * r_hi + r_lo

        if b1 < self.fade_in_bytes:
            fade = b1 / self.fade_in_bytes
        elif b1 >= self.fade_out_bytes:
            fade = (len(frames) - b1) / self.fade_in_bytes
        else:
            fade = 1

        return fade * left, fade * right


class SoundSource:
    def __init__(self, *files, fade_time=FADE_TIME):
        self.files = list(files)
        self.finished = bool(files)
        self.current_file = None
        self.open_file()
        self.fade_frames = fade_time * FRAMERATE
        self.frame_index = 0
        self.fade_index = 0
        self.gap_frames = 0

    def get_frame(self):
        """Return the next frame as a pair of numbers between 0 and 65536"""
        if self.gap_frames:
            # We are in an gap
            self.gap_frames -= 1
            return 0, 0

        if self.fade_frames:
            # We are in an fade. TODO
            return 0, 0


    def open_file(self):
        if self.files:
            with wave.open(self.files.pop(0)) as fp:
                self.next_file = fp.readframes(fp.nframes())
