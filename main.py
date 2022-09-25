"""
Playing with animations for guitar scales.

todo:
Accommodate rhythm (e.g. When the Sun Goes Down).
Abstraction(s) for building up arrays of positions.
    Simplify by not specifying string numbers explicitly? [(1, 7), (3, 9)] => [7, None, 9]
    Chord shapes (e.g. major seven, minor), tranposed to given root.
Arpeggios two octaves over each chord in a given key (see lesson videos).
Generate following animations:
    Solos: Californication, Zephyr Song.
Module(s).
    Remove all global state.
    Separate anything common to guitar, piano etc. (music theory).
    Separate repo per component?
Translate notes to string and fret numbers and vice versa.
    Define standard tuning EADGBe (accommodate other tunings e.g. drop D).
    But keep fret position representation: chords not necessarily "logical".
Handle open strings as fret 0. marker at left edge (nut)?
Define pentatonic shape then transpose to different scales/root notes.
Extend to other modes (Dorian etc.).
Input raw audio, extract notes (e.g. via librosa chromagram).
    Then change transparency of dots based on volume and animate at say 25 FPS (rather than binary note on/off).
Improve images:
    Own guitar has 21 frets: truncate fretboard image?
    Increase contrast: white neck, grey frets, black markers.
    Generate the neck image from the edges array (can then translate to SVG).
    Include transparency of marker.
Include bends, hammer-ons, pull-offs.
Generate synchronised audio.
Type annotations.
"""

import os.path

from PIL import Image

# Measured positions of fretboard edges and strings.
fret_edges = [140,266,385,497,603,703,797,886,970,1049,1124,1195,1261,1324,1384,1440,1493,1543,1590,1634,1676,1716,1753,1789]
string_centres = [25,53,81,109,137,165]
num_strings = len(string_centres)

# todo: deal with A#/Bb: identity will depend on which scale.
chroma = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]
major_intervals = [1, 1, 2, 1, 1, 1, 2]

# def position_to_note(string, fret):
#     note = "C"
#     octave = 4
#     return (note, octave)

# def major_scale(key):
#     pass

# def minor_scale(key):
#     pass

# def arpeggio(key):
#     pass

def imread(filename):
    return Image.open(os.path.join(folder, filename))

# Load input images.
folder = 'images'
frets = imread('guitar-fretboard.png')
marker = imread('circle.png')
marker_width, marker_height = marker.size

def imsave(image, filename):
    image.save(os.path.join(folder, filename))

def calculate_offset(string, fret):
    """Calculate the (x, y) offset needed to position the marker on a given string and fret.""" 
    x = fret_edges[fret - 1] - marker_width
    y = string_centres[num_strings - string] - marker_height//2
    return (x, y)

def render_image(positions):
    """Render an image of the neck with markers at the given positions."""
    output = frets.copy()
    for (string, fret) in positions:
        offset = calculate_offset(string, fret)
        output.paste(marker, offset)
    return output

def render_images(sequence):
    """Given a sequence of string and fret numbers, generate corresponding images.
    
    todo:
    Input validation
    Error handling
    Generator rather than load all images at once.
    """
    images = []
    for _, positions in enumerate(sequence):
        image = render_image(positions)
        images.append(image)
    return images

def append_reversed_sequence(sequence):
    """Given a sequence, reverse it and append it (without repeating the middle position).

    Useful to e.g. take an ascending scale and descend it.
    
    todo: remove last image also if looping animation?
    """
    return sequence + sequence[-2::-1]

def bpm_to_milliseconds(bpm):
    """Convert beats per minute (BPM) to milliseconds."""
    return 60000/bpm

def animate_images(images, filename, bpm=60):
    """Given array of images, save as animation (GIF)."""
    duration = bpm_to_milliseconds(bpm)
    images[0].save(os.path.join(folder, filename), append_images=images[1:], duration=duration, save_all=True, optimize=True, loop=0)

def main():
    # Define pentatonic shape (tuples of (string, fret)).
    # todo: transpose to given key/root note.
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

    # Descend the scale too.
    # sequence = append_reversed_sequence(pentatonic_ascending)
    # bpm = 120
    # filename = f'pentatonic-bpm={bpm:d}.gif'

    # When the Sun Goes Down.
    # todo: define sequence B, D#7, Emaj7, D#m, Emaj7, D#m, C#m, F#7, E7, D#m, C#m, D#m.
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
    
    # Generate images and save as animation.
    # todo: generate incrementally rather than load all images into memory.
    images = render_images(sequence)
    animate_images(images, filename, bpm)

if __name__ == '__main__':
    main()
