"""
Draws images of a guitar fretboard with given notes marked.

TODO:
Wrap in CLI?
Show notes of open strings (tuning).
MVP is static image of one scale one position, all markers same.
Text labels on notes (note name or scale degree).
Scale numbers as required.
Draw dimensions with padding etc.
Optimise dimensions and DPI for phone and tablet (save both).
How to integrate sheet music? Just paste as image?
Enforce minimum sizes, line widths (not sub-pixel).
Specify bounding box, dimensions within it normalised to [0, 1],
    use this to combine e.g. fretboard and piano in single frame.
Adapt to different string numbers: bass, ukelele, extended guitar.
Change to SVG?
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
marker_radius = 40
image_width = 2220
image_height = 1080
# TODO: optimise for tablet and laptop dimensions also.


# TODO: transform in here so always drawing in norm space?
def draw_line(context, start, finish):
    context.move_to(start.x, start.y)
    context.line_to(finish.x, finish.y)
    context.stroke()


def draw_circle(context, centre: Point, r):
    context.arc(centre.x, centre.y, r, 0, 2*math.pi)
    context.fill()


def get_fret_x_position(fret):
    # TODO: combine into (string, fret) -> (x, y) lookup?
    # TODO: transform here?
    return fret/num_frets


def get_string_y_position(string):
    # TODO: combine into (string, fret) -> (x, y) lookup?
    # TODO: transform here?
    return (string - 1)/(num_strings - 1)


def draw_frets(context, normed_to_global):
    for fret in range(num_frets + 1):
        u = get_fret_x_position(fret)
        start = normed_to_global(Point(u, 0))
        finish = normed_to_global(Point(u, 1))
        draw_line(context, start, finish)


def draw_strings(context, normed_to_global):
    for string in range(num_strings):
        v = get_string_y_position(string + 1)
        start = normed_to_global(Point(0, v))
        finish = normed_to_global(Point(1, v))
        draw_line(context, start, finish)


# TODO: refactor for single note so they can be different colours.
def draw_notes(context, notes: List[NoteMarker], normed_to_global):
    for note in notes:
        r = 40  # TODO: account for this in padding. Make it smaller than closest fret.
        u = get_fret_x_position(note.fret)  # TODO: minus r!
        v = get_string_y_position(note.string)
        centre = normed_to_global(Point(u, v))
        centre.x -= marker_radius
        draw_circle(context, centre, marker_radius)


# TODO: grey: colour as arg. Common function to set colour. Named values.
def draw_inlays(context: cairo.Context, normed_to_global):
    def get_inlay_x_position(fret):
        return (get_fret_x_position(fret) + get_fret_x_position(fret - 1))/2
    
    inlay_radius = marker_radius/2

    rgb = 0.7
    grey = (rgb, rgb, rgb)
    context.set_source_rgb(*grey)
    
    for fret in [3, 5, 7, 9, 15, 17, 19, 21]:
        u = get_inlay_x_position(fret)
        v = 0.5
        centre = normed_to_global(Point(u, v))
        draw_circle(context, centre, inlay_radius)
    
    # Double inlay at 12th fret.
    u = get_inlay_x_position(12)
    offset = 0.2
    v1 = 0.5 - offset
    v2 = 0.5 + offset
    centre1 = normed_to_global(Point(u, v1))
    centre2 = normed_to_global(Point(u, v2))
    draw_circle(context, centre1, inlay_radius)
    draw_circle(context, centre2, inlay_radius)


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


def chord_string_to_note_markers(chord_string):
    note_markers = []
    for i, char in enumerate(chord_string):
        string = i + 1
        if char != "x":
            fret = int(char)
            note_markers.append(NoteMarker(string, fret))
    return note_markers


def main():
    # Create a new surface and context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, image_width, image_height)
    context = cairo.Context(surface)

    # Establish coordinate system transforms.
    # TODO: make padding a ratio of image size not absolute pixels.
    padding_horizontal = 50
    padding_vertical = 250
    top_left = Point(padding_horizontal + 2*marker_radius, padding_vertical + marker_radius)
    bottom_right = Point(image_width - padding_horizontal, image_height - padding_vertical - marker_radius)
    _, normed_to_global = get_transforms(top_left, bottom_right)

    # Set white background
    white = (1, 1, 1)
    context.set_source_rgb(*white)
    context.paint()

    # Set antialiasing mode
    context.set_antialias(cairo.ANTIALIAS_BEST)

    # Set line width and color.
    # TODO: move into draw functions?
    black = (0, 0, 0)
    line_width = 5  # TODO: scale with image.
    context.set_line_width(line_width)
    context.set_line_cap(cairo.LINE_CAP_ROUND)

    draw_inlays(context, normed_to_global)
    context.set_source_rgb(*black)
    draw_frets(context, normed_to_global)
    draw_strings(context, normed_to_global)

    # Draw some notes.
    # TODO: add more chords!
    G = '300023'
    notes = chord_string_to_note_markers(G)
    draw_notes(context, notes, normed_to_global)

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
