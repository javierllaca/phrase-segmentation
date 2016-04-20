import numpy as np
import os
from vectorizer import make_training_example


def get_paths(dirs):
    for base in dirs:
        for path in os.listdir(base):
            yield '{}/{}'.format(base, path)


def make_training_examples(dirs, window_size):
    Xs, ys = [], []
    for path in get_paths(dirs):
        try:
            X, y = make_training_example(path, window_size, 'C')
            Xs.append(X)
            ys.append(y)
        except Exception as exception:
            print path
    return Xs, ys


def make_dataset(Xs, ys):
    m = sum(len(y) for y in ys)
    n = Xs[0].shape[1]
    X = np.zeros((m, n))
    y = np.zeros(m)
    i = 0
    for j in range(len(Xs)):
        m_j, n_j = Xs[j].shape
        X[i:i + m_j, 0:n_j] = Xs[j]
        y[i:i + m_j] = ys[j]
        i += m_j
    return X, y


# First Viennese School
dirs = [
    'corpora/bm/mxl/Mozart, Wolfgang Amadeus',
    'corpora/bm/mxl/Haydn, Franz Josef',
    'corpora/bm/mxl/Beethoven, Ludwig Van'
]


def main():
    Xs, ys = make_training_examples(dirs, 10)
    X, y = make_dataset(Xs, ys)
    X_path, y_path = 'dataset/X.npy', 'dataset/y.npy'
    m, n = X.shape
    np.save(X_path, X)
    np.save(y_path, y)
    print '{} musical examples'.format(len(Xs))
    print '{}x{} feature matrix -> {}'.format(X_path)
    print '{}-element class label vector -> {}'.format(y_path)


if __name__ == '__main__':
    main()
