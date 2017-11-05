import os
from . import get_files

COMMAND = '/usr/local/bin/sox {infile} -c 2 -b 16 -t wav -r 48000 {outfile}'


def normalize_files(root='samples', output='normal_samples', dry_run=False):
    for infile in get_files.get_files(root):
        outfile = os.path.relpath(infile, root)
        outfile = os.path.join(output, outfile)
        outfile = os.path.splitext(outfile)[0] + '.wav'
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        command = COMMAND.format(**locals())
        if dry_run:
            print(command)
        else:
            os.system(command)
            print(infile, '->', outfile)


if __name__ == '__main__':
    normalize_files()
