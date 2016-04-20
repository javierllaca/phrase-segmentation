import os
import re
import urllib

urllib.urlretrieve(
    'http://www.multimedialibrary.com/barlow/all_barlow.asp',
    'index.html'
)

regex = re.compile(
    r'<LI><A HREF="JavaScript: openMIDI\(\'(MIDIFiles/Midi\d+.mid)\'\)" '
    r'class="head1">(.*):&nbsp;&nbsp;(.*)</A><BR>'
)

composers = {}

for line in open('index.html', 'r'):
    match = regex.match(line.strip())
    if match:
        url, composer, title = match.groups()
        piece = title, url
        if composer in composers:
            composers[composer].append(piece)
        else:
            composers[composer] = [piece]

os.mkdir('mid')
for composer, pieces in composers.items():
    dir_path = 'mid/{}'.format(composer)
    os.mkdir(dir_path)
    print dir_path
    for title, url in pieces:
        path = '{}/{}.mid'.format(dir_path, title)
        full_url = 'http://www.multimedialibrary.com/barlow/{}'.format(url)
        urllib.urlretrieve(full_url, path)
        print '\t{} -> {}'.format(full_url, path)
