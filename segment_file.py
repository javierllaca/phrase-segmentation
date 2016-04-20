import matplotlib.pyplot as plt
import music21
import mxl_reader
from sklearn.externals import joblib
from sys import argv
import util
from vectorizer import make_feature_matrix


def color_score(score, eop, color='#ff0000'):
    i = 0
    for measure, element in mxl_reader.get_elements(score):
        if isinstance(element, music21.note.Note):
            if eop[i] == 1:
                element.color = color
            i += 1


def find_first(a, x):
    for i in range(len(a)):
        if a[i] == x:
            return i
    return -1


def segment(model, path, window_size, show=True):
    eop = []
    tokens = mxl_reader.read_mxl_file(path)
    X = make_feature_matrix(tokens, window_size)
    while True:
        y = model.predict(X)
        i = find_first(y, 1)
        if i < 0:
            break
        eop.extend(y[:i + 1])
        tokens = tokens[i + 1:, ]
        X = make_feature_matrix(tokens, window_size)
    eop.extend(y)
    if show:
        score = music21.converter.parse(path)
        color_score(score, eop)
        score.show()
    return eop


def make_plot(model, path, window_size):
    eop = segment(model, path, window_size, show=False)
    plt.plot(range(len(eop)), eop, '-o')
    plt.show()


def main(model_path, music_path, window_size, plot=False):
    model = joblib.load(model_path)
    if plot:
        make_plot(model, music_path, window_size)
    else:
        segment(model, music_path, window_size)


if __name__ == '__main__':
    if len(argv) == 4:
        main(argv[1], argv[2], int(argv[3]))
    elif len(argv) == 5:
        plot = argv[4] == '-p'
        print plot
        main(argv[1], argv[2], int(argv[3]), plot)
    else:
        print (
            'Usage: python {} <model_path> <music_path> '
            '<window_size> [-p]'.format(argv[0])
        )
