from math import log2


class Note:
    NOTE_NAMES = 'C', 'D', 'E', 'F', 'G', 'A', 'B'
    SUB = str.maketrans("-0123456789", "₋₀₁₂₃₄₅₆₇₈₉")
    NOTE_SEMITONE_STEPS = 0, 2, 4, 5, 7, 9, 11
    ACCIDENTALS = {-1: "♭", 0: "", 1: "♯"}

    def __init__(self, note_index: int, octave: int, accidental=0):
        self.note_index = note_index
        self.octave = octave
        self.accidental = accidental

    def __str__(self):
        accidental = f"{self.ACCIDENTALS[self.accidental]}"
        octave = f"{str(self.octave).translate(self.SUB)}"
        return ''.join([self.note_name, accidental, octave])
    
    @property
    def note_name(self):
        return self.NOTE_NAMES[self.note_index]
    
    @property
    def is_natural(self):
        return self.accidental == 0
    
    @property
    def semitone_value(self):
        # designed to return the midi number for each note (69 for A4)
        val_from_octave = 12 * (self.octave + 1)
        val_from_semitone = self.NOTE_SEMITONE_STEPS[self.note_index]
        val_from_accidental = self.accidental
        return val_from_octave + val_from_accidental + val_from_semitone

    def enharmonic_note(self):
        if self.is_natural:
            return self
        return self.note_from_semitone_value(self.semitone_value, self.accidental == 1)

    def note_to_freq(self, a4=440.0):
        return round(a4 * 2 ** ((self.semitone_value - 69) / 12), 3)

    @classmethod
    def note_from_semitone_value(cls, n, flat=False):
        octave, semitones, acc = *divmod(n, 12), 0
        octave -= 1
        if semitones not in cls.NOTE_SEMITONE_STEPS:
            if flat:
                semitones, acc = semitones + 1, acc - 1
            else:
                semitones, acc = semitones - 1, acc + 1
        index = cls.NOTE_SEMITONE_STEPS.index(semitones)
        return Note(index, octave, acc)
    
    @classmethod
    def freq_to_note(cls, freq, a4=440.0):
        cents_from_a4 = 1200 * log2(freq / a4)
        semitones = round(cents_from_a4 / 100)
        cents = cents_from_a4 - 100 * semitones
        note = cls.note_from_semitone_value(69 + semitones)
        return note, round(cents, 2)

note_a4 = Note(5, 4)
