from typing import Dict, List, NamedTuple

from chroma import Chroma, chroma_list, len_chroma
from fretboard import FretboardPosition
from notes import Note


# Standard tuning.
standard_tuning = [
    Note(Chroma.E, 2),
    Note(Chroma.A, 2),
    Note(Chroma.D, 3),
    Note(Chroma.G, 3),
    Note(Chroma.B, 3),
    Note(Chroma.E, 4)
]

class GuitarTuning:
    """Guitar tuning: convert from string and fret to note and vice versa.
    
    todo:
    Invert string numbers to follow convention that high E is 1.
    Use MIDI note numbers instead to simplify?
    """
    def __init__(self, open_strings=standard_tuning, num_frets=21):
        self._open_strings = open_strings
        self._num_strings = len(open_strings)  # todo: validate at six? Or allow fewer for e.g. bass, ukelele?
        self._num_frets = num_frets

        # Build lookup tables to convert from position to note and vice versa.
        # TODO: refactor to key on note and position i.e. tuples, not nested dict with separate chroma and octave.
        # TODO: test changes using create_video.py.
        self._positions_to_notes: Dict[FretboardPosition, Note] = {}
        self._notes_to_positions: Dict[Note, List[FretboardPosition]] = {}
        for string in range(1, self._num_strings + 1):
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
                
                # Store lookup value for this position.
                position = FretboardPosition(string, fret)
                note = Note(chroma, octave)
                self._positions_to_notes[position] = note

                # If no entry for this note in inverse lookup, initialise it.
                if note not in self._notes_to_positions.keys():
                    self._notes_to_positions[note] = []
                
                # Now safe to add note to inverse lookup.
                # Append because there may be multiple positions for the same note.
                self._notes_to_positions[note].append(position)
    
    def note_to_positions(self, note: Note) -> List[FretboardPosition]:
        """Given a note (chroma and octave), return the corresponding positions."""
        try:
            return self._notes_to_positions[note]
        except KeyError:
            print(f'The note {note} is not available in this tuning.')
    
    def position_to_note(self, position: FretboardPosition) -> Note:
        """Given a string and fret, return the corresponding note.
        
        todo: Change input validation to just check whether key is in lookup dict?
        todo: typing
        """
        if position.fret < 0:
            raise ValueError(f'fret must be >= 0 (which represents the open string).')

        if position.fret > self._num_frets:
            raise ValueError(f'fret must be <= {self._num_frets}')
        
        if position.string < 1:
            raise ValueError(f'string must be >= 1.')
        
        if position.string > self._num_strings:
            raise ValueError(f'string must be <= {self._num_strings}.')
        
        return self._positions_to_notes[position]
