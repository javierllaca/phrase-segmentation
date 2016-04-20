import csv
import os
import re
import subprocess


def musescore_convert(src_path, dst_path):
    return subprocess.call([
        '/Applications/MuseScore 2.app/Contents/MacOS/mscore',
        src_path,
        '-o',
        dst_path
    ])


regex = re.compile(r'(.*)\.mid')

failed = []

os.mkdir('mxl')
for composer in os.listdir('mid'):
    composer_path = 'mid/{}'.format(composer)
    if not os.path.isdir('mxl/{}'.format(composer)):
        os.mkdir('mxl/{}'.format(composer))
    for piece in os.listdir(composer_path):
        match = regex.match(piece)
        if match:
            src_path = 'mid/{}/{}'.format(composer, piece)
            dst_path = 'mxl/{}/{}.mxl'.format(composer, match.group(1))
            if not os.path.isfile(dst_path):
                if musescore_convert(src_path, dst_path) != 0:
                    failed.append((src_path, dst_path))
                else:
                    print '{} -> {}'.format(src_path, dst_path)

with open('error.csv', 'w') as error_file:
    for src_path, dst_path in failed:
        error_file.write('"{}","{}"\n'.format(src_path, dst_path))
