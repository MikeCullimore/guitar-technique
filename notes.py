"""
notes.py

todo:
Add minor variants: harmonic, melodic.
Separate file scales.py? Just rename?
Convert note and octave to pitch (configurable tuning, start with concert pitch).
Capture circle of fifths?
"""

from chroma import Chroma, chroma_list, len_chroma
from guitar_tuning import GuitarTuning

semitone = 1
tone = 2
minor_third = 3
major_third = 4
intervals_major = [tone, tone, semitone, tone, tone, tone, semitone]
intervals_minor = [tone, semitone, tone, tone, semitone, tone, tone]
minor_pentatonic_scale_degrees = [1, 3, 4, 5, 7]  # (Of the natural minor scale with the same root.)
major_pentatonic_scale_degrees = [1, 2, 3, 5, 6]  # (Of the natural minor scale with the same root.)

def get_notes_in_scale(chroma, intervals):
    i = chroma_list.index(chroma)
    notes = [chroma]
    for interval in intervals:
        j = (i + interval) % len_chroma
        notes.append(chroma_list[j])
        i = j
    return notes

def major_scale(chroma):
    return get_notes_in_scale(chroma, intervals_major)

def natural_minor_scale(chroma):
    return get_notes_in_scale(chroma, intervals_minor)

def minor_pentatonic_scale(root):
    """Get the minor pentatonic scale on the given root."""
    # Start with natural minor scale with same root.
    minor = natural_minor_scale(root)

    # Select the required degrees of the minor scale.
    return [minor[d - 1] for d in minor_pentatonic_scale_degrees]

def major_pentatonic_scale(root):
    """Get the major pentatonic scale on the given root."""
    # Start with major scale with same root.
    major = major_scale(root)

    # Select the required degrees of the minor scale.
    return [major[d - 1] for d in major_pentatonic_scale_degrees]

def get_major_triad(root):
    return get_notes_in_scale(root, [major_third, minor_third])

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
    notes = major_scale(chroma)
    notes = notes[:-1]  # Truncate the octave.
    print(f'Notes in the key of {chroma.name}: {notes_str(notes)}')
    
    # Select notes in triad (starting on each root in the key).
    # todo: given triad, infer character (major? minor? diminished?).
    # todo: separate function to get triad for just one root in given key.
    # todo: capture intervals (major third, perfect fifth).
    print(f'Triads:')
    n = len(notes)
    root = 1
    third = 3
    fifth = 5
    for i, note in enumerate(notes):
        # Select notes from scale.
        # triad = [notes[((i + j - 1) % n)] for j in [root, third, fifth]]
        
        # Alternative: get triad directly from known intervals.
        triad = get_major_triad(note)
        print(notes_str(triad))

def notes_str(notes):
    return ', '.join([note.name for note in notes])

def test_tuning_lookups():
    tuning = GuitarTuning()
    # x = tuning.position_to_note(1, 1)
    x = tuning.note_to_positions(Chroma.A, 3)
    print(x)

def main():
    # test_tuning_lookups()
    
    # scale = minor_pentatonic_scale(Chroma.C)
    # scale = major_pentatonic_scale(Chroma.C)
    # print(notes_str(scale))

    get_triads_in_major_key(Chroma.D)

if __name__ == '__main__':
    main()
