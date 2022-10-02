"""
notes.py

todo:
Add pentatonic scale.
Separate file scales.py?
Convert chroma to note names, accounting for key (e.g. is note C# or D♭?).
Convert note and octave to pitch (configurable tuning, start with concert pitch).
"""

from chroma import Chroma, chroma_list, len_chroma
from guitar_tuning import GuitarTuning

semitone = 1
tone = 2
minor_third = 3
major_third = 4
intervals_major = [tone, tone, semitone, tone, tone, tone, semitone]
intervals_minor = [tone, semitone, tone, tone, semitone, tone, tone]

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

def get_notes_in_key(chroma, intervals):
    i = chroma_list.index(chroma)
    notes = [chroma]
    for interval in intervals:
        j = (i + interval) % len_chroma
        notes.append(chroma_list[j])
        i = j
    return notes

def get_notes_in_major_key(chroma):
    return get_notes_in_key(chroma, intervals_major)

def get_notes_in_minor_key(chroma):
    return get_notes_in_key(chroma, intervals_minor)

def get_major_triad(root):
    return get_notes_in_key(root, [major_third, minor_third])

def get_triads_in_major_key(chroma):
    """For a given major key, get the triads (for arpeggio exercise).
    
    todo:
    Need to know character of each triad to know which pattern to use.
        Possible to work it out so not tied into EADGBe tuning?
    Generate in all keys.
    Animation for each.
    """
    # Triads in key of D:
    # D major: D F# A
    # E minor: E G B
    # F# minor: F# A C#
    # G major: G B D
    # A major: A C# E
    # B minor: B D F#
    # C# (half?) diminished: C# E G
    
    # Notes in key of D: D E F# G A B C#
    notes = get_notes_in_major_key(chroma)
    notes = notes[:-1]  # Truncate the octave.
    print(f'Notes in the key of {chroma.name}: {", ".join([n.name for n in notes])}')
    
    # Select notes in triad (starting on each root in the key).
    # todo: given triad, infer character (major? minor? diminished?).
    # todo: separate function to get triad for just one root in given key.
    # todo: capture intervals (major third, perfect fifth).
    print(f'Triads:')
    n = len(notes)
    for i, _ in enumerate(notes):
        triad = [notes[i]]
        for j in [2, 4]:
            triad.append(notes[(i + j) % n])
        print(', '.join([note.name for note in triad]))
    
    # root = 1
    # third = 3
    # fifth = 5
    
    triad = get_major_triad(Chroma.D)
    print(', '.join([note.name for note in triad]))

def main():
    # test_tuning_lookups()
    get_triads_in_major_key(Chroma.D)

if __name__ == '__main__':
    main()
