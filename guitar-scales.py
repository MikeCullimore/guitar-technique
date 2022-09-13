"""
guitar-scales.py

todo:
Include transparency of circle.
Translate notes to string and fret numbers.
Animate sequence of several images.
How to handle open strings? Circle at left edge (nut)?
Define pentatonic shape then transpose to different scales/root notes.
"""

import os.path
from PIL import Image

folder = 'images'

# Measured positions of fretboard edges and strings.
fret_edges = [140,266,385,497,603,703,797,886,970,1049,1124,1195,1261,1324,1384,1440,1493,1543,1590,1634,1676,1716,1753,1789]
string_centres = [25,53,81,109,137,165]
num_strings = len(string_centres)

def imread(fname):
    return Image.open(os.path.join(folder, fname))

def imsave(image, fname):
    image.save(os.path.join(folder, fname))

def calculate_offset(string, fret, w, h):
    return (fret_edges[fret - 1] - w, string_centres[num_strings - string] - h//2)

def main():
    # Load images.
    frets = imread('guitar-fretboard.png')
    circle = imread('circle.png')
    
    w, h = circle.size
    # string = 5
    # fret = 12
    # offset = calculate_offset(string, fret, w, h)

    # frets.putalpha(255)
    # frets.paste(circle, offset)
    # frets.save('tmp.png')

    pentatonic = [
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

    for i, (string, fret) in enumerate(pentatonic):
        offset = calculate_offset(string, fret, w, h)
        output = frets.copy()
        output.paste(circle, offset)
        imsave(output, f'pentatonic-{i+1:02}.png')

if __name__ == '__main__':
    main()
