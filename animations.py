"""
Playing with animations for guitar scales.

todo:
Handle open strings as fret 0. marker at left edge (nut)?
All positions for each scale.
Power chords.
Text printout of neck (see e.g. https://en.wikipedia.org/wiki/Power_chord)
Abstraction(s) for building up arrays of positions.
    Simplify by not specifying string numbers explicitly? [(1, 7), (3, 9)] => [7, None, 9]
    Chord shapes (e.g. major seven, minor), transposed to given root.
    Similarly for arpeggios.
    Define pentatonic shape then transpose to different scales/root notes.
    Given a key, return all the chords in that key.
        Break down: return all the notes, then get chord for given note.
Generate following images:
    For every chroma value, mark all positions.
Generate following animations:
    Californication
    Zephyr Song
    I Want You (She's So Heavy)
Show which notes coming next? (Show left hand shape then highlight each when played.)
Accommodate rhythm (e.g. When the Sun Goes Down).
Reverse string numbers? Standard is low E string is 6 not 1?
Improve images:
    Adapt to vertical neck for chord diagrams.
    Own guitar has 21 frets: truncate fretboard image?
    Increase contrast: white neck, grey frets, black markers.
    Generate the neck image from the edges array (can then translate to SVG).
    Include transparency of marker.
    Display note names, intervals.
    Equally spaced frets? (Don't need realism, better use of space.) As option?
    Option to look at guitar as if held by someone else.
Extend to other modes (Dorian etc.).
Input raw audio, extract notes (e.g. via librosa chromagram).
    Turns out this is a very challenging, not fully solved, problem.
    Then change transparency of dots based on volume and animate at say 25 FPS (rather than binary note on/off).
Include bends, hammer-ons, pull-offs.
Type annotations.
"""

from neck_renderer import NeckRenderer
from scales import append_reversed_sequence

def animate(sequence, filename, bpm):
    """Generate images and save as animation.
    
    todo:
    Generate incrementally rather than load all images into memory.
    Change input format to array of positions and onsets, use same input to audio.
        ASCII tab?
        Flexible enough?
    """
    neck_renderer = NeckRenderer()
    neck_renderer.animate(sequence, filename, bpm)

def pentatonic():
    """Minor pentatonic shape."""
    # todo: transpose to given key/root note.
    # todo: convert to list of frequencies.
    pentatonic_ascending = [
        [(1, 12)],
        [(1, 15)],
        [(2, 12)],
        [(2, 14)],
        [(3, 12)],
        [(3, 14)],
        [(4, 12)],
        [(4, 14)],
        [(5, 12)],
        [(5, 15)],
        [(6, 12)],
        [(6, 15)],
    ]
    sequence = append_reversed_sequence(pentatonic_ascending)
    bpm = 120
    filename = f'pentatonic-bpm={bpm:d}.gif'
    animate(sequence, filename, bpm)

def when_the_sun_goes_down():
    """Arctic Monkeys: don't believe the hype! ;)"""
    B = [(1, 7), (2, 9), (3, 9), (4, 8), (5, 7), (6, 7)]
    C_SHARP_MINOR = [(2, 4), (3, 6), (4, 6), (5, 5), (6, 4)]
    D_SHARP_MINOR = [(2, 6), (3, 8), (4, 8), (5, 7), (6, 6)]
    D_SHARP_7 = [(2, 6), (3, 8), (4, 6), (5, 8), (6, 6)]
    E_7 = [(2, 7), (3, 9), (4, 7), (5, 9), (6, 7)]
    E_MAJOR_7 = [(2, 7), (3, 9), (4, 8), (5, 9), (6, 7)]
    F_SHARP_7 = [(2, 9), (3, 11), (4, 9), (5, 11), (6, 9)]
    sequence = [B, D_SHARP_7, E_MAJOR_7, D_SHARP_MINOR, E_MAJOR_7, D_SHARP_MINOR, C_SHARP_MINOR, F_SHARP_7, E_7, D_SHARP_MINOR, C_SHARP_MINOR, D_SHARP_MINOR]
    filename = 'When the Sun Goes Down.gif'
    bpm = 120/4
    animate(sequence, filename, bpm)

def arpeggios():
    # Arpeggios over two octaves in the key of D (D E F# G A B C#).
    # todo: show shape for current arpeggio then highlight each note within it.
    # todo: generate these given the key.
    # todo: generate in all keys.
    # D major: D F# A
    # E minor: E G B
    # F# minor: F# A C#
    # G major: G B D
    # A major: A C# E
    # B minor: B D F#
    # C# half dim: C# E G
    # D major 
    sequence = [
        [(2, 5)],
        [(3, 4)],
        [(4, 2)],
        [(5, 3)],
        [(6, 2)],
        [(6, 5)],
        [(2, 7)],
        [(3, 5)],
        [(4, 4)],
        [(5, 5)],
        [(6, 3)],
        [(6, 7)],
        [(2, 9)],
        [(3, 7)],
        [(4, 6)],
        [(5, 7)],
        [(6, 5)],
        [(6, 9)],
        [(2, 10)],
        [(3, 9)],
        [(4, 7)],
        [(5, 8)],
        [(6, 7)],
        [(6, 10)],
        [(2, 12)],
        [(3, 11)],
        [(4, 9)],
        [(5, 10)],
        [(6, 9)],
        [(6, 12)],
        [(2, 14)],
        [(3, 12)],
        [(4, 11)],
        [(5, 12)],
        [(6, 10)],
        [(6, 14)],
        [(2, 16)],
        [(3, 14)],
        [(4, 12)],
        [(5, 14)],
        [(6, 12)],
        [(6, 15)],
        [(2, 17)],
        [(3, 16)],
        [(4, 14)],
        [(5, 15)],
        [(6, 14)],
        [(6, 17)],
    ]
    bpm = 60
    filename = 'Arpeggios over two octaves in D.gif'
    animate(sequence, filename, bpm)

def main():
    pentatonic()
    # when_the_sun_goes_down()
    # arpeggios()

if __name__ == '__main__':
    main()
