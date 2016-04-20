import music21
from music21.key import KeySignature
from music21.interval import Interval, notesToInterval
from music21.meter import TimeSignature
from music21.note import Note
from music21.pitch import Pitch
from music21.stream import Measure

import numpy as np
import util


def read_mxl_file(path, target_key=None):
    tokens = []
    score = music21.converter.parse(path)
    for measure, element in get_elements(score):
        if isinstance(element, KeySignature) and target_key:
            pc = element.pitchAndMode[0].pitchClass
            target_pc = Pitch(target_key).pitchClass
            interval = util.optimal_interval(pc, target_pc)
            print pc, target_pc, interval
        elif isinstance(element, TimeSignature):
            numerator = element.numerator
            denominator = element.denominator
        elif isinstance(element, Note):
            if target_key:
                element.pitch = element.pitch.transpose(interval)
            tokens.append((
                element.pitch.midi,
                element.pitch.pitchClass,
                element.duration.quarterLength,
                util.measure_duration(
                    element.duration.quarterLength,
                    numerator,
                    denominator
                ),
                element.beat,
                measure
            ))
    return np.array(tokens)


def get_elements(score):
    measure = 1
    for token in score.parts[0]:  # monophonic input -> 1 part
        if isinstance(token, Measure):
            for element in token._elements:
                yield measure, element
            measure += 1
