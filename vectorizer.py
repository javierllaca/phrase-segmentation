import csv
from mxl_reader import read_mxl_file
import numpy as np
import sys
import util


def load_cuddy_luney_data(path):
    ratings = {}
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for interval_a, interval_b, rating in reader:
            ratings[(int(interval_a), int(interval_b))] = float(rating)
    return ratings


def fetch_rating(a):
    return ratings.get((a[0], a[1])) or 0.0


def window_key_correlations(pitches, durations):
    m, _ = pitches.shape
    k = np.zeros((m, 24))
    for i in range(m):
        k[i, :] = util.key_corrrelations(pitches[i, :], durations[i, :])
    return k


def windows(v, m, size, pad=0, default=0):
    w = np.zeros((m, size))
    w.fill(default)
    for j in range(m):
        i = j - size + pad if j >= size else 0
        k = j - i + pad
        w[j, size - k:size] = v[i:j + pad]
    return w


def make_feature_matrix(tokens, window_size):
    m, _ = tokens.shape

    # unpack token matrix
    pitch, pc, length, duration, beat, measure = map(
        np.array,
        tokens.T.tolist()
    )

    # Token windows
    pitch_window = np.fliplr(windows(pitch, m, window_size, 1, -1))
    pc_window = np.fliplr(windows(pc, m, window_size, 1, -1))
    length_window = np.fliplr(windows(length, m, window_size, 1))
    duration_window = np.fliplr(windows(duration, m, window_size, 1))
    beat_window = np.fliplr(windows(beat, m, window_size, 1))
    measure_window = np.fliplr(windows(measure, m, window_size, 1))

    # Interval windows
    opi_window = windows(util.opi_vector(pitch), m, window_size - 1)
    upi_window = windows(util.upi_vector(pitch), m, window_size - 1)
    opci_window = windows(util.opci_vector(pitch), m, window_size - 1)
    upci_window = windows(util.upci_vector(pitch), m, window_size - 1)

    # Cuddy-Luney interval expectation
    cuddy_luney = np.apply_along_axis(fetch_rating, 1, opi_window[:, -2:])
    cuddy_luney = cuddy_luney.reshape((m, 1)) # make matrix

    # Key correlation windows
    window_key_corrs = window_key_correlations(pitch_window, length_window)

    return np.concatenate((
        pitch_window,
        pc_window,
        length_window,
        duration_window,
        beat_window,
        measure_window,
        opi_window,
        upi_window,
        opci_window,
        upci_window,
        cuddy_luney,
        window_key_corrs,
    ), 1)


def make_training_example(path, window_size, target_key=None, y=None):
    tokens = read_mxl_file(path, target_key)
    X = make_feature_matrix(tokens, window_size)
    m, _ = X.shape
    return X, y or np.array([0] * (m - 1) + [1])


def main(path, window_size):
    tokens = read_mxl_file(path)
    X = make_feature_matrix(tokens, window_size)
    print X.shape
    np.savetxt('temp', X, '%.2f', ',')


ratings = load_cuddy_luney_data('cuddy-lunney/data.csv')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        print 'usage: python {} <path> <window_size>'.format(sys.argv[0])
