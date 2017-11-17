import pydub, sys, wave
from . import get_files, util


def format_time(duration, use_hours=False):
    m, s = divmod(round(duration), 60)
    if use_hours:
        h, m = divmod(m, 60)
        return '%d:%02d:%02d' % (h, m, s)
    else:
        return '%02d:%02d' % (m, s)


def file_durations():
    result = {}
    for name, files in sorted(get_files.get_files_by_category().items()):
        total_duration = 0
        for file in files:
            try:
                duration = pydub.AudioSegment.from_file(file).duration_seconds
            except KeyboardInterrupt:
                raise
            except:
                print('ERROR: couldn\'t read file', file, file=sys.stderr)
            else:
                total_duration += duration
                duration = format_time(duration)
                result.setdefault(name, {})[file] = duration
                print(duration, 'for', file, file=sys.stderr)

        print(name, '--', format_time(total_duration, True), file=sys.stderr)

    return result


if __name__ == '__main__':
    durations = file_durations()
    util.json_dump(durations)
