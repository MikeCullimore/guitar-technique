"""
guitar-scales.py

todo:
Include transparency of circle.
Translate notes to string and fret numbers.
Animate sequence of several images.
"""

from PIL import Image

# Measured positions of fretboard edges and strings.
fret_edges = [140,266,385,497,603,703,797,886,970,1049,1124,1195,1261,1324,1384,1440,1493,1543,1590,1634,1676,1716,1753,1789]
string_centres = [25,53,81,109,137,165]

def imread(fname):
    return Image.open(fname)

def main():
    # Load images.
    frets = imread('guitar-fretboard.png')
    circle = imread('circle.png')

    w, h = circle.size
    string = 5
    fret = 12
    num_strings = len(string_centres)
    offset = (fret_edges[fret - 1] - w, string_centres[num_strings - string] - h//2)
    
    frets.paste(circle, offset)
    frets.save('tmp.png')

if __name__ == '__main__':
    main()
