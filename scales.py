"""
scales.py

todo:
Number of octaves as arg.
Combine this with note to neck position lookup to generate scale exercises.
    Or shift focus to scale patterns instead?
    For chords, needs to be shapes not patterns!
Differentiate between enharmonic notes e.g. C# and D♭.
Add minor variants: harmonic, melodic.
Capture circle of fifths?
Chord inversions (separate file?).
Specify octave of root note. Default to 4.
    Then transpose by octave(s).
Power chords.
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
    """todo: account for octave: initial as arg, then each time counter loops round chroma list, increment. Default: 4."""
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

def append_reversed_sequence(sequence, loop=True):
    """Given a sequence, reverse it and append it (without repeating the middle position).

    Useful to e.g. take an ascending scale and descend it.
    """
    stop = -len(sequence) if loop else None
    return sequence + sequence[-2:stop:-1]

def notes_str(notes):
    return ', '.join([note.name for note in notes])

def test_tuning_lookups():
    tuning = GuitarTuning()
    # x = tuning.position_to_note(1, 1)
    x = tuning.note_to_positions(Chroma.A, 3)
    print(x)

def scale_to_neck_positions():
    """Convert scale to neck positions, choosing best route where many available.
    
    todo:
    Need to specify an octave?
    Need to append the root note an octave higher.
    """
    scale = minor_pentatonic_scale(Chroma.E)
    print(notes_str(scale))

def main():
    # test_tuning_lookups()
    
    # scale = minor_pentatonic_scale(Chroma.C)
    # scale = major_pentatonic_scale(Chroma.C)
    # print(notes_str(scale))

    # get_triads_in_major_key(Chroma.D)

    scale_to_neck_positions()

if __name__ == '__main__':
    main()
