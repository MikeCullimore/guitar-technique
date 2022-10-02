"""
notes.py

todo:
Given key, return chords in that key.
Convert chroma to note names, accounting for key (e.g. is note C# or D♭?).
Convert note and octave to pitch (configurable tuning, start with concert pitch).
Port to Rust?
"""

from chroma import Chroma, chroma_list, len_chroma
from guitar_tuning import GuitarTuning

# Type aliases: https://docs.python.org/3/library/typing.html
# todo: possible to impose length limits e.g. Tuning is a list of *six* strings?
Octave = int
Note = tuple[Chroma, Octave]
Tuning = list[Note]
String = int
Fret = int
Position = tuple[String, Fret]

def test_tuning_lookups():
    tuning = GuitarTuning()
    # x = tuning.position_to_note(1, 1)
    x = tuning.note_to_positions(Chroma.A, 3)
    print(x)

def get_arpeggios_major_key(chroma):
    """For a given major key, get the triads (for arpeggio exercise).
    
    todo:
    Separate smaller functions e.g. major key.
    Generate in all keys.
    Animation for each.
    """
    # D major: D F# A
    # E minor: E G B
    # F# minor: F# A C#
    # G major: G B D
    # A major: A C# E
    # B minor: B D F#
    # C# half dim: C# E G
    # D E F# G A B C#
    semitone = 1
    tone = 2
    intervals_major = [tone, tone, semitone, tone, tone, tone, semitone]
    i = chroma_list.index(chroma)
    notes = [chroma]
    for interval in intervals_major:
        j = (i + interval) % len_chroma
        notes.append(chroma_list[j])
        i = j
    
    # for note in notes:
    #     print(note.name)
    
    notes = notes[:-1]  # Truncate the octave.
    n = len(notes)
    for i, _ in enumerate(notes):
        triad = [notes[i]]
        for j in [2, 4]:
            triad.append(notes[(i + j) % n])
        for note in triad:
            print(note.name)
        print()

def main():
    # test_tuning_lookups()
    get_arpeggios_major_key(Chroma.D)

if __name__ == '__main__':
    main()
