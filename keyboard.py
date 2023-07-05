"""
Draw images of a piano keyboard with given notes marked.

TODO:
Animate. GIF? Video? (webm?)
Combine with fretboard in single image.
Allow arbitrary first and last key.
    Work out range of guitar in standard tuning with same # frets as own (22?) and match it. C2 to C6?
    Default to range of full 88 key piano (because both ends are odd!). Simpler to just do whole octaves?
    Do same for bass.
Define vertices for each note then repeat for octaves.
    White notes should include shape of black not just rectangle drawn over.
    Check by colouring each key blue separately.
    Function to draw note: input note and colour (including transparency).
        Separate border and fill?
Operator overloads for point (add, subtract).
Option to print note names on keys.
    Or scale degrees.
Encapsulate coordinate transformations in drawing functions.
SVG equivalent (for React).
"""

from dataclasses import dataclass
import math
from typing import List

import cairo


# TODO: use this to define range and address individual notes (e.g. to colour).
@dataclass
class Note:
    noteName: str
    octave: int

@dataclass
class Point:
    x: float
    y: float

    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f})"


# TODO: no global state!

# Phone screen dimensions.
image_width = 2220
image_height = 1080

# Tablet screen dimensions.
# image_width = 2160
# image_height = 1620

# Tablet screen dimensions.
# image_width = 2560
# image_height = 1600

def get_transforms(top_left: Point, bottom_right: Point):
    # TODO: do we need global_to_normed?
    def global_to_normed(point: Point):
        u = (point.x - top_left.x)/(bottom_right.x - top_left.x)
        v = (point.y - top_left.y)/(bottom_right.y - top_left.y)
        return Point(u, v)

    def normed_to_global(point: Point):
        x = top_left.x + point.x*(bottom_right.x - top_left.x)
        y = top_left.y + point.y*(bottom_right.y - top_left.y)
        return Point(x, y)

    return global_to_normed, normed_to_global


def normed_to_global_list(points: List[Point], normed_to_global):
    return [normed_to_global(p) for p in points]


def draw_polygon(context: cairo.Context, vertices: List[Point], fill=True):
    start = vertices[0]
    context.move_to(start.x, start.y)
    for vertex in vertices[1:]:
        context.line_to(vertex.x, vertex.y)
    context.close_path()
    if fill:
        context.fill()
    else:
        context.stroke()


def main():
    # Create a new surface and context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, image_width, image_height)
    context = cairo.Context(surface)

    # Set white background
    white = (1, 1, 1)
    context.set_source_rgb(*white)
    context.paint()

    # Set antialiasing mode
    context.set_antialias(cairo.ANTIALIAS_BEST)

    # Set line width and color.
    black_key_colour = (0, 0, 0)
    # t = 0.7
    # black_key_colour = (t, t, t)
    line_width = 5  # TODO: scale with image.
    context.set_line_width(line_width)
    context.set_source_rgb(*black_key_colour)

    # Establish coordinate system transforms.
    # TODO: make padding a ratio of image size not absolute pixels.
    # TODO: enforce aspect ratio limits for keyboard so never squashed.
    padding_horizontal = 200
    padding_vertical = 100
    top_left = Point(padding_horizontal, padding_vertical)
    bottom_right = Point(image_width - padding_horizontal, image_height/2)  #  - padding_vertical)
    _, normed_to_global = get_transforms(top_left, bottom_right)

    # Define keyboard dimensions.
    golden_ratio = 2/(1 + math.sqrt(5))
    num_octaves = 4
    num_white_keys = 7*num_octaves
    white_key_width = 1/num_white_keys
    black_key_width = golden_ratio*white_key_width
    
    # Draw white keys (naive: rectangles).
    for i in range(num_white_keys):
        left = i*white_key_width
        right = left + white_key_width
        vertices = normed_to_global_list([
            Point(left, 0),
            Point(right, 0),
            Point(right, 1),
            Point(left, 1),
            Point(left, 0)
        ], normed_to_global)
        draw_polygon(context, vertices, fill=False)
    
    # Draw black keys.
    c = black_key_width/4
    d = c
    offsets = num_octaves*[-c, c, -d, 0, d]
    multiples = []
    for octave in range(num_octaves):
        for black_key_position in [1, 2, 4, 5, 6]:
            multiples.append(7*octave + black_key_position)
    for multiple, offset in zip(multiples, offsets):
        left = multiple*white_key_width - black_key_width/2 + offset
        right = left + black_key_width
        vertices = normed_to_global_list([
                Point(left, 0),
                Point(right, 0),
                Point(right, golden_ratio),
                Point(left, golden_ratio),
                Point(left, 0)
            ], normed_to_global)
        draw_polygon(context, vertices)

    # Save the image as PNG
    surface.write_to_png("keyboard.png")


if __name__ == '__main__':
    main()
