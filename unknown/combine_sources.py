from . import sound_source


class CombineSources:
    def __init__(self, fade_frames, *files, wave_open=None, verbose=True):
        self.files = list(files)
        self.fade_frames = fade_frames
        self.wave_open = wave_open
        self.source = self.next_source()
        self.incoming_source = None
        self.verbose = verbose

    def __iter__(self):
        return self

    def __next__(self):
        """Return the next frame as a pair of numbers between 0 and 65536"""
        if not self.source:
            raise StopIteration

        if not self.incoming_source and self.source.in_fade_out():
            self.incoming_source = self.next_source()

        try:
            frame = next(self.source)
        except StopIteration:
            self.source = self.incoming_source or self.next_source()
            if not self.source:
                raise StopIteration

            self.incoming_source = None
            frame = next(self.source)

        if not self.incoming_source:
            return frame

        l1, r1 = frame
        l2, r2 = next(self.incoming_source)
        return l1 + l2, r1 + r2

    def next_source(self):
        if self.files:
            file = self.files.pop(0)
            print('Reading file',
        return self.files and sound_source.SoundSource(
            , self.fade_frames, self.wave_open)
