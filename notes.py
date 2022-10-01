"""
notes.py

todo:
Invert string numbers to follow convention that high E is 1.
Convert chroma to note names, accounting for key (e.g. is note C# or D♭?).
Convert note and octave to pitch (configurable tuning, start with concert pitch).
Given key, return chords in that key.
Port to Rust?
"""

from enum import Enum, auto

class Chroma(Enum):
    C = auto()
    C_SHARP = auto()
    D = auto()
    D_SHARP = auto()
    E = auto()
    F = auto()
    F_SHARP = auto()
    G = auto()
    G_SHARP = auto()
    A = auto()
    A_SHARP = auto()
    B = auto()

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
        self._num_strings = len(open_strings)  # todo: validate at six? Or allow fewer for e.g. bass, ukelele?
        self._num_frets = num_frets

        # Build lookup tables to convert from position to note and vice versa.
        self._position_to_notes = {}
        self._notes_to_positions = {}
        for string in range(1, self._num_strings + 1):
            # Initialise empty lookup for this string.
            self._position_to_notes[string] = {}
            
            # Get open string.
            chroma_open, octave_open = self._open_strings[string - 1]
        
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

                # If no entry for this chroma in inverse lookup, initialise it.
                if chroma not in self._notes_to_positions.keys():
                    self._notes_to_positions[chroma] = {}
                
                # If no entry for this octave and this chroma, initialise it.
                if octave not in self._notes_to_positions[chroma].keys():
                    self._notes_to_positions[chroma][octave] = []
                
                # Now safe to add note to inverse lookup.
                # Append because there may be multiple positions for the same note.
                self._notes_to_positions[chroma][octave].append((string, fret))
    
    def note_to_positions(self, chroma, octave):
        """Given a note (chroma and octave), return the corresponding positions.

        todo:
        Make octave optional, or have separate method chroma_to_positions?
        """
        try:
            return self._notes_to_positions[chroma][octave]
        except KeyError:
            print(f'The note {chroma}{octave} is not available in this tuning.')
    
    def position_to_note(self, string, fret):
        """Given a string and fret, return the corresponding note.
        
        todo: Change input validation to just check whether key is in lookup dict?
        """
        if fret < 0:
            raise ValueError(f'fret must be >= 0 (which represents the open string).')

        if fret > self._num_frets:
            raise ValueError(f'fret must be <= {self._num_frets}')
        
        if string < 1:
            raise ValueError(f'string must be >= 1.')
        
        if string > self._num_strings:
            raise ValueError(f'string must be <= {self._num_strings}.')
        
        return self._position_to_notes[string][fret]

def main():
    tuning = GuitarTuning()

    # Testing.
    # x = tuning.position_to_note(1, 1)
    x = tuning.note_to_positions(Chroma.A, 3)
    print(x)

if __name__ == '__main__':
    main()