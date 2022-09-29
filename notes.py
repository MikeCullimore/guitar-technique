"""
notes.py

todo:
Convert chroma to note names, accounting for key (e.g. is note C# or D♭?).
Convert note and octave to pitch (configurable tuning, start with concert pitch).
Convert note and octave to string and fret numbers, throwing error if out of range.
    If multiple matches, return them all. Separate algorithm to choose which given context of other notes.
    Easier to define other way, from string and fret to note? Build up that mapping then invert it.
Given key, return chords in that key.
"""

from enum import Enum, auto

class Chroma(Enum):
    A = auto()
    A_SHARP = auto()
    B = auto()
    C = auto()
    C_SHARP = auto()
    D = auto()
    D_SHARP = auto()
    E = auto()
    F = auto()
    F_SHARP = auto()
    G = auto()
    G_SHARP = auto()

chroma_list = list(Chroma)
len_chroma = len(chroma_list)

# Type aliases: https://docs.python.org/3/library/typing.html
# todo: possible to impose length limits e.g. Tuning is a list of *six* strings?
Octave = int
Note = tuple[Chroma, Octave]
Tuning = list[Note]
String = int
Fret = int
Position = tuple[String, Fret]

# Standard tuning.
E2 = (Chroma.E, 2)
A2 = (Chroma.A, 2)
D3 = (Chroma.D, 3)
G3 = (Chroma.G, 3)
B3 = (Chroma.B, 3)
E4 = (Chroma.E, 4)
standard_tuning = [E2, A2, D3, G3, B3, E4]

class GuitarTuning:
    def __init__(self, open_strings=standard_tuning, num_frets=21):
        self._open_strings = open_strings
        self._num_strings = len(open_strings)  # todo: validate at six? Or allow fewer for e.g. ukelele?
        self._num_frets = num_frets

        # Build lookup tables to convert from position to note and vice versa.
        # todo: build inverse lookup.
        self._position_to_notes = {}
        for string in range(self._num_strings):
            # Initialise empty lookup for this string.
            self._position_to_notes[string] = {}
            
            # Get open string.
            chroma_open, octave_open = self._open_strings[string]
        
            # Which index in chroma list is open string?
            array_offset = chroma_list.index(chroma_open)
            
            # Fret 0 is the open string so loop over 0, 1, ..., num_frets.
            for fret in range(self._num_frets + 1):
                # Counting frets from that open string chroma, what is resulting
                # chroma including octave offset?
                octave_offset, array_index = divmod(fret + array_offset, len_chroma)
                chroma = chroma_list[array_index]
        
                # Add octave offset to octave of open string.
                octave = octave_open + octave_offset
                self._position_to_notes[string][fret] = (chroma, octave)
        # print(self._position_to_notes)
        # print(self._position_to_notes[0][0])
    
    def find_note(self, note):
        """todo: inverse mapping to get (string, fret) combinations (plural!)."""
        pass
    
    def position_to_note(self, string, fret):
        """Given a string and fret, return the corresponding note.
        
        todo: use lookup table.
        """
        if fret > self._num_frets:
            raise ValueError(f'Fret must be <= {self._num_frets}')

def main():
    num_frets = 21
    tuning = GuitarTuning(num_frets=num_frets)
    
    for string, lookup in tuning._position_to_notes.items():
        print(f'String: {string}')
        # fret = 0
        # chroma, octave = lookup[fret]
        # print(f'Chroma of string {string}, fret {fret}: {chroma}')
        for fret, v in lookup.items():
            chroma, octave = v
            print(f'Fret {fret}: {chroma.name}{octave}')
        print()

if __name__ == '__main__':
    main()
