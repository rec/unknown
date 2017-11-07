from . import sound_source

# If FADE_TIME is positive, then there is a fade between consecutive pairs of
# source files of that many seconds.
#
# If SPACING_TIME is positive, then the start of the next source file is
# delayed by that many seconds.  The default is 0
#
# For example, if FADE_TIME = 0 and SPACING_TIME = 0, then each sample is
# played right after the other with no pause.
#
# If FADE_TIME = 3 and SPACING_TIME = 0 then starting 3 seconds before the end
# of each file, the first sample fades out and the second one fades in.
#
# If FADE_TIME = 0 and SPACING_TIME = 3 then each sample is played
# right after the other with a three second pause pause.
#
# If FADE_TIME = 3 and SPACING_TIME = 3 then each sample fades to nothing
# in its last three seconds, and then the next sample fades in in 3 seconds.


class CombineSources:
    def __init__(self, *files, fade_time=3, wave_open=None):
        self.files = list(files)
        self.finished = bool(files)
        self.source = self.next_source()
        self.incoming_source = None
        self.fade_frames = fade_time * sound_source.FRAME_RATE
        self.wave_open = wave_open

    def __iter__(self):
        return self

    def __next__(self):
        """Return the next frame as a pair of numbers between 0 and 65536"""
        frame = self.source.next_frame()

        if not frame:
            self.source = self.incoming_source or self.next_source()
            self.incoming_source = None
            frame = self.source and self.source.next_frame()
            if not frame:
                raise StopIteration

        if not self.incoming_source and self.source.in_fade_out():
            self.incoming_source = self.next_source()

        if not self.incoming_source:
            return frame

        l1, r1 = frame
        l2, r2 = self.incoming_source.next_frame()
        return l1 + l2, r1 + r1

    def next_source(self):
        return self.files and sound_source.SoundSource(
            self.files.pop(0), self.fade_frames, self.wave_open)
