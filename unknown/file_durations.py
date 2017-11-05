import os, pydub
from . import get_files


def print_time(duration, name, use_hours):
    m, s = divmod(round(duration), 60)
    if use_hours:
        h, m = divmod(m, 60)
        print('%d:%02d:%02d - %s' % (h, m, s, name))
    else:
        print('%02d:%02d - %s' % (m, s, name))


def file_durations():
    for name, files in sorted(get_files.get_files_by_category().items()):
        total_duration = 0
        for file in files:
            try:
                duration = pydub.AudioSegment.from_file(file).duration_seconds
            except KeyboardInterrupt:
                raise
            except:
                print('ERROR: couldn\'t read file', file)
            else:
                print_time(duration, os.path.basename(file), True)
                total_duration += duration

        print_time(total_duration, name, True)
        print()


if __name__ == '__main__':
    file_durations()
