"""
Playing with animations for guitar scales.

todo:
Separate the rendering of a circle on the fretboard.
    Optional more than one (chords).
Function to take sequence of notes, output animation with given name.
Include transparency of circle.
Translate notes to string and fret numbers.
Handle open strings as fret 0. Circle at left edge (nut)?
Define pentatonic shape then transpose to different scales/root notes.
Extend to other modes (Dorian etc.).
Function to descend a given scale.
Input raw audio, extract notes (e.g. via librosa chromagram).
    Then change transparency of dots based on volume and animate at say 25 FPS (rather than binary note on/off).
Type annotations.
Module(s).
"""

import os.path
from PIL import Image

folder = 'images'

def imread(filepath):
    return Image.open(os.path.join(folder, filepath))

# Measured positions of fretboard edges and strings.
fret_edges = [140,266,385,497,603,703,797,886,970,1049,1124,1195,1261,1324,1384,1440,1493,1543,1590,1634,1676,1716,1753,1789]
string_centres = [25,53,81,109,137,165]
num_strings = len(string_centres)

# Load input images.
frets = imread('guitar-fretboard.png')
marker = imread('circle.png')
marker_width, marker_height = marker.size

class ImageRenderer:
    def render(self, string, fret):
        """Render a marker on the given string at the given fret."""
        offset = self._calculate_offset(string, fret)
        output = frets.copy()
        output.paste(marker, offset)
        return output
    
    def _calculate_offset(self, string, fret):
        """Calculate the offset to a given string and fret from the top left corner."""
        x = fret_edges[fret - 1] - marker_width
        y = string_centres[num_strings - string] - marker_height//2
        return (x, y)

def main():
    ir = ImageRenderer()
    im = ir.render(1, 1).show()
    # print(type(im))

if __name__ == '__main__':
    main()
