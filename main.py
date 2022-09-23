"""
Playing with animations for guitar scales.

todo:
Convert BPM tempo to frame duration ms.
Module(s).
    Remove all global state.
Translate notes to string and fret numbers and vice versa.
    Define standard tuning EADGBe (accommodate other tunings e.g. drop D).
Separate the rendering of a marker on the fretboard.
    Optional more than one at once (chords).
Function to take sequence of notes, output animation with given name.
Include transparency of marker.
Handle open strings as fret 0. marker at left edge (nut)?
Define pentatonic shape then transpose to different scales/root notes.
Extend to other modes (Dorian etc.).
Function to descend a given scale.
Input raw audio, extract notes (e.g. via librosa chromagram).
    Then change transparency of dots based on volume and animate at say 25 FPS (rather than binary note on/off).
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

animation_default_kwargs = {'save_all': True, 'optimize': True, 'duration': 500, 'loop': 0}

def imsave(image, filename):
    image.save(os.path.join(folder, filename))

def calculate_offset(string, fret, marker_width, marker_height):
    """Calculate the (x, y) offset needed to position the marker on a given string and fret.""" 
    x = fret_edges[fret - 1] - marker_width
    y = string_centres[num_strings - string] - marker_height//2
    return (x, y)

def generate_images(sequence, marker_width, marker_height):
    """Given a sequence of string and fret numbers, generate corresponding images.
    
    todo:
    Input validation
    Error handling
    Generator rather than load all images at once.
    """
    images = []
    for i, (string, fret) in enumerate(sequence):
        offset = calculate_offset(string, fret, marker_width, marker_height)
        output = frets.copy()
        output.paste(marker, offset)
        images.append(output)
    return images

def append_reversed_sequence(sequence):
    """Given a sequence, reverse it and append it (without repeating the middle position).

    Useful to e.g. take an ascending scale and descend it."""
    return sequence + sequence[-2::-1]

def animate_images(images, filename, kwargs=animation_default_kwargs):
    """Given array of images, save as animation (GIF)."""
    images[0].save(os.path.join(folder, filename), append_images=images[1:], **animation_default_kwargs)

def main():
    # Define pentatonic shape (tuples of (string, fret)).
    # todo: transpose to given key/root note.
    pentatonic_ascending = [
        (1, 12),
        (1, 15),
        (2, 12),
        (2, 14),
        (3, 12),
        (3, 14),
        (4, 12),
        (4, 14),
        (5, 12),
        (5, 15),
        (6, 12),
        (6, 15),
    ]

    # Descend the scale too.
    pentatonic_ascending_descending = append_reversed_sequence(pentatonic_ascending)

    # Generate images for each position in the scale.
    images = generate_images(pentatonic_ascending_descending, marker_width, marker_height)
    
    # Save animation.
    # todo: generate incrementally rather than load all images into memory.
    animate_images(images, 'pentatonic.gif')

if __name__ == '__main__':
    main()
