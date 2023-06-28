# TODO: MVP is static image of one scale one position, all markers same.
# TODO: draw notes.
# TODO: text labels on notes (note name or scale degree).
# TODO: scale numbers as required.
# TODO: draw dimensions with padding etc.
# TODO: separate function to get XY positions for given fret and string.
# TODO: optimise dimensions and DPI for phone and tablet (save both).
# TODO: how to integrate sheet music? Just paste as image?
# TODO: make indexing for frets and notes consistent (missing fret 0?).

from dataclasses import dataclass
import math
from typing import List

import cairo

@dataclass
class NoteMarker:
    string: int
    fret: int


# TODO: no global state!
num_strings = 6
num_frets = 22
padding = 5
c2 = -0.13827529
c1 = 7.52403813
b = (100 - 2*padding)/100
# strokeWidth = .3
string_sizes = [.1, .15, .2, .25, .3, .35]  # TODO: adapt for bass etc. (just define min and max then interpolate).
scaling = 5  # TODO: remove need for this (proper dimensions).


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
    string_spacing = get_fret_x_position(num_frets) - get_fret_x_position(num_frets - 1)
    return scaling*(padding + string_spacing*string)


def draw_frets(context):
    y1 = get_string_y_position(1)
    y2 = get_string_y_position(num_strings)
    for i in range(num_frets):
        x = get_fret_x_position(i + 1)
        draw_line(context, x, y1, x, y2)


def draw_strings(context):
    x1 = get_fret_x_position(1)
    x2 = get_fret_x_position(num_frets)
    for i in range(num_strings):
        context.set_line_width(string_sizes[i])
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


def main():
    # Create a new surface and context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
    context = cairo.Context(surface)

    # Set white background
    context.set_source_rgb(1, 1, 1)  # White color
    context.paint()

    # Set antialiasing mode
    context.set_antialias(cairo.ANTIALIAS_BEST)

    # Set line width and color
    context.set_line_width(2)
    context.set_source_rgb(0, 0, 0)  # Black color

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