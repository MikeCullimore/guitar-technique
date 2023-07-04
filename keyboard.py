"""
Draw images of a piano keyboard with given notes marked.

TODO:
Allow arbitrary first and last key.
Define vertices for each note then repeat for octaves.
    White notes should include shape of black not just rectangle drawn over.
Operator overloads for point (add, subtract).
Option to print note names on keys.
"""

from dataclasses import dataclass
import math
from typing import List

import cairo

@dataclass
class NoteMarker:
    string: int
    fret: int

@dataclass
class Point:
    x: float
    y: float

    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f})"


# TODO: no global state!
image_width = 2220
image_height = 1080
# TODO: optimise for tablet and laptop dimensions also.


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
    black = (0, 0, 0)
    line_width = 5  # TODO: scale with image.
    context.set_line_width(line_width)
    context.set_source_rgb(*black)

    # Establish coordinate system transforms.
    # TODO: make padding a ratio of image size not absolute pixels.
    padding_horizontal = 200
    padding_vertical = 100
    top_left = Point(padding_horizontal, padding_vertical)
    bottom_right = Point(image_width - padding_horizontal, image_height - padding_vertical)
    _, normed_to_global = get_transforms(top_left, bottom_right)

    # Define keyboard dimensions.
    golden_ratio = 2/(1 + math.sqrt(5))
    num_white_keys = 7
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
    c = 0.01
    d = 0.02
    offsets = [-c, c, -d, 0, d]
    for k, offset in zip([1, 2, 4, 5, 6], offsets):
        left = k*white_key_width - black_key_width/2 + offset
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
