"""
Draws images of a guitar fretboard with given notes marked.

TODO:
Adapt to different string numbers: bass, ukelele, extended guitar.
Equal fret spacing: simpler.
Show notes of open strings (tuning).
MVP is static image of one scale one position, all markers same.
Text labels on notes (note name or scale degree).
Scale numbers as required.
Draw 
Draw dimensions with padding etc.
Separate function to get XY positions for given fret and string.
Optimise dimensions and DPI for phone and tablet (save both).
How to integrate sheet music? Just paste as image?
Make indexing for frets and notes consistent (missing fret 0?).
Enforce minimum sizes, line widths (not sub-pixel).
Specify bounding box, dimensions within it normalised to [0, 1],
    use this to combine e.g. fretboard and piano in single frame.
Can lines have rounded ends? If not, make own? Or switch to SVG?
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
num_strings = 6
num_frets = 22
padding = 5
c2 = -0.13827529
c1 = 7.52403813
b = (100 - 2*padding)/100
# strokeWidth = .3
scaling = 20  # TODO: remove need for this (proper dimensions).
image_width = 2220
image_height = 1080


def draw_line(context, x1, y1, x2, y2):
    context.move_to(x1, y1)
    context.line_to(x2, y2)
    context.stroke()


def draw_circle(context, x, y, r):
    context.arc(x, y, r, 0, 2*math.pi)
    context.stroke()


def get_fret_x_position(fret):
    return scaling*(padding + b*(c1*fret + c2*fret*fret))


def get_string_y_position(string):
    # Make string spacing match closest fret spacing.
    string_spacing = get_fret_x_position(num_frets) - get_fret_x_position(num_frets - 1)
    return padding + string_spacing*string


def draw_frets(context):
    y1 = get_string_y_position(1)
    y2 = get_string_y_position(num_strings)
    for i in range(num_frets + 1):
        x = get_fret_x_position(i)
        draw_line(context, x, y1, x, y2)


def draw_strings(context):
    x1 = get_fret_x_position(0)
    x2 = get_fret_x_position(num_frets)
    for i in range(num_strings):
        y = get_string_y_position(i + 1)
        draw_line(context, x1, y, x2, y)


def draw_notes(context, notes: List[NoteMarker]):
    for note in notes:
        r = .6*scaling
        x = get_fret_x_position(note.fret) - r
        y = get_string_y_position(note.string)
        if note.fret == 0:
            stroke_width = 0.1*scaling
            context.set_line_width(stroke_width)
            draw_circle(context, x - stroke_width, y, r)
        else:
            draw_circle(context, x, y, r)  # TODO: fill


def get_transforms(top_left: Point, bottom_right: Point):
    def global_to_normed(point: Point):
        u = (point.x - top_left.x)/(bottom_right.x - top_left.x)
        v = (point.y - top_left.y)/(bottom_right.y - top_left.y)
        return Point(u, v)

    def normed_to_global(point: Point):
        x = top_left.x + point.x*(bottom_right.x - top_left.x)
        y = top_left.y + point.y*(bottom_right.y - top_left.y)
        return Point(x, y)

    return global_to_normed, normed_to_global


def debug_transform():
    # TODO: Box wrapper to handle transforms underneath? Draw in (u, v).
    tl = Point(0, 0)
    br = Point(image_width, image_height)
    global_to_normed, normed_to_global = get_transforms(tl, br)
    a = global_to_normed(tl)
    b = global_to_normed(br)
    print(a)
    print(b)

    br2 = Point(1, 1)
    c = normed_to_global(br2)
    print(c)


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
    # TODO: move into draw functions.
    black = (0, 0, 0)
    line_width = 5  # TODO: scale with image.
    context.set_line_width(line_width)
    context.set_source_rgb(*black)

    draw_frets(context)
    draw_strings(context)

    # Draw some notes.
    notes = [
        NoteMarker(1, 0),
        NoteMarker(2, 5)
    ]
    draw_notes(context, notes)

    # # Set rectangle properties
    # context.set_line_width(2)
    # context.set_source_rgb(1, 0, 0)  # Red color

    # # Draw a rectangle
    # context.rectangle(200, 200, 100, 200)
    # context.stroke()

    # # Set circle properties
    # context.set_line_width(2)
    # context.set_source_rgb(0, 0, 1)  # Blue color

    # # Draw a circle
    # context.arc(150, 350, 50, 0, 2 * 3.1415)
    # context.stroke()

    # # Set text properties
    # context.set_font_size(24)
    # context.set_source_rgb(0, 0.8, 0)  # Green color

    # # Draw text
    # context.move_to(100, 50)
    # context.show_text("Hello, World!")

    # Save the image as PNG
    surface.write_to_png("guitar_fretboard.png")


if __name__ == '__main__':
    main()
    # debug_transform()