import os, numpy, sys, wave, wavio
from . import constants


def framecount(file):
    return wave.open(file).getnframes()


def read(file, dtype='float'):
    wave = wavio.read(file)
    assert wave.sampwidth == 2 and wave.rate == constants.FRAMERATE

    left = wave.data[:, 0].astype(dtype)
    right = wave.data[:, 1].astype(dtype) if wave.data.shape[1] > 1 else None
    return left, right


def write(file, data, verbose=False):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    verbose and print('Starting to write', file)
    wavio.write(file, data, constants.FRAMERATE, scale='raw', sampwidth=2)
    verbose and print('Written')


def combine(file, samples):
    n = len(samples)
    left, *middle, right = samples

    for i, sample in enumerate(middle):
        ratio = (i + 1) / (n - 1)
        left += (1 - ratio) * sample
        right += ratio * sample

    left /= (n / 2)
    right /= (n / 2)

    write(file, numpy.column_stack((left, right)))

COMBINE = """\
/usr/local/bin/sox {input}\
 --channels 2 --combine merge {output}\
 remix 1v0.5,2v0.375,3v0.125 2v0.125,3v0.375,4v0.5"""


def sox_combine(outfile, infiles):
    command = COMBINE.format(input=' '.join(infiles), output=outfile)
    print('Combining with:', command)
    os.system(command)
    print('Done')


def read_combine_and_write(outfile, *infiles, dtype='float'):
    print('Combining', *(infiles + ('into file', outfile)))
    print('Reading')
    samples = [read(f, dtype)[0] for f in infiles]
    print('Combining')
    combine(outfile, samples)
    print('Done')


if __name__ == '__main__':
    read_combine_and_write(*sys.argv[1:])
