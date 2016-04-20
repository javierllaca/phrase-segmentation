import numpy as np


major = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
minor = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]


def opi(x, y):
    return y - x


def opi_vector(x):
    return interval_vector(x, opi)


def upi(x, y):
    return abs(opi(x, y))


def upi_vector(x):
    return interval_vector(x, upi)


def opci(x, y):
    return opi(x, y) % 12


def opci_vector(x):
    return interval_vector(x, opci)


def upci(x, y):
    return np.minimum(opci(x, y), opci(y, x))


def upci_vector(x):
    return interval_vector(x, upci)


def interval_vector(x, reducer):
    return reducer(x[:-1], x[1:])


def pitch_class_distribution(pitches, durations):
    x = np.zeros(12)
    for i in range(len(pitches)):
        x[pitches[i] % 12] += durations[i]
    return x


def key_corrrelations(pitches, durations):
    """ Krumhansl-Schmuckler key-finding algorithm"""
    x = pitch_class_distribution(pitches, durations)
    c = np.zeros(24)
    for i in range(12):
        r = np.roll(x, -i)
        c[2 * i] = np.corrcoef(major, r)[0, 1]
        c[2 * i + 1] = np.corrcoef(minor, r)[0, 1]
    return c


def measure_duration(quarter_length, numerator, denominator):
    return float(quarter_length * denominator) / (4 * numerator)


def test_measure_duration():
    assert util.measure_duration(0.5, 3, 4) == 1 / 6.
    assert util.measure_duration(0.5, 4, 4) == 1 / 8.
    assert util.measure_duration(0.5, 12, 8) == 1 / 12.
    assert util.measure_duration(1, 6, 8) == 1 / 3.


def optimal_interval(x, y):
    """Compute shortest-distance interval between pitch classes a and b"""
    i = upci(x, y)
    return i if (x + i) % 12 == y else -i


def test_optimal_interval():
    assert optimal_interval(4, 8) == 4
    assert optimal_interval(8, 4) == -4
    assert optimal_interval(0, 5) == 5
    assert optimal_interval(0, 7) == -5
    assert optimal_interval(9, 0) == 3
