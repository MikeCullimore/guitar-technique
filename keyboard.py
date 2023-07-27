"""
Draw images of a piano keyboard with given notes marked.

TODO:
Animate. GIF? Video? (webm?)
    Start with single frame, given list of notes and their colours.
Combine with fretboard in single image.
Allow arbitrary first and last key.
    Work out range of guitar in standard tuning with same # frets as own (22?) and match it. C2 to C6?
    Default to range of full 88 key piano (because both ends are odd!). Simpler to just do whole octaves?
    Do same for bass.
Option to print labels on keys, could be note names, scale degrees, fingering.
Encapsulate coordinate transformations in drawing functions.
SVG equivalent (for React).
Sketch relevant music data representations (chord sheets, TAB, MIDI) and mappings between them.
"""

from dataclasses import dataclass
from enum import Enum
import math
from typing import Dict, List, NamedTuple

import cairo
from chroma import Chroma

from fretboard import chord_string_to_fretboard_positions
from guitar_tuning import GuitarTuning
from notes import Note


class KeyboardDimensions(NamedTuple):
    num_octaves: float
    white_key_width: float
    black_key_width: float
    black_key_height: float
    offset_1: float  # TODO: better name
    offset_2: float  # TODO: better name


class Colour(NamedTuple):
    red: int
    green: int
    blue: int

    def __str__(self):
        return f"Colour(red={self.red}, green={self.green}, blue={self.blue})"


# TODO: should this be NamedTuple also?
# TODO: operator overloads to allow addition, subtraction, scaling. Does pycairo provide?
@dataclass
class Point:
    x: float
    y: float

    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f})"


def get_transform(top_left: Point, bottom_right: Point):
    def normed_to_global(point: Point):
        x = top_left.x + point.x*(bottom_right.x - top_left.x)
        y = top_left.y + point.y*(bottom_right.y - top_left.y)
        return Point(x, y)

    return normed_to_global


def normed_to_global_list(points: List[Point], normed_to_global):
    return [normed_to_global(p) for p in points]


# TODO: why does this not stroke _and_ fill?
def draw_polygon(context: cairo.Context, vertices: List[Point], fill_colour: Colour=None, line_colour: Colour=None):
    if line_colour is not None:
        start = vertices[0]
        context.move_to(start.x, start.y)
        for vertex in vertices[1:]:
            context.line_to(vertex.x, vertex.y)
        context.close_path()    
        context.set_source_rgb(*line_colour)
        context.stroke()

    # TODO: it shouldn't be necessary to draw the shape again for the fill to render.
    if fill_colour is not None:
        start = vertices[0]
        context.move_to(start.x, start.y)
        for vertex in vertices[1:]:
            context.line_to(vertex.x, vertex.y)
        context.close_path()
        context.set_source_rgb(*fill_colour)
        context.fill()


# TODO: use to draw black keys in default colour (grey? not black: don't want emphasis).
def is_black_key(pitch: Chroma):
    return pitch in [Chroma.A_SHARP, Chroma.C_SHARP, Chroma.D_SHARP, Chroma.F_SHARP, Chroma.G_SHARP]

# TODO: remove?
def is_white_key(pitch: Chroma):
    return not is_black_key(pitch)


KeyVerticesLookup = Dict[Chroma, List[Point]]

# TODO: define template for each shape then add X offset for octave.
# TODO: also scale in X for number of octaves? (Define keys in x in [0, 1].)
# TODO: separate file.
# TODO: type for shape to enable e.g. translation.
def get_key_vertices_lookup(keyboard_dimensions: KeyboardDimensions) -> KeyVerticesLookup:
    lookup: KeyVerticesLookup = {}

    bkh = keyboard_dimensions.black_key_height
    
    u1 = 0
    u3 = keyboard_dimensions.white_key_width
    u2 = u3 - keyboard_dimensions.black_key_width/2 - keyboard_dimensions.offset_1
    lookup[Chroma.C] = [
        Point(u1, 0),
        Point(u2, 0),
        Point(u2, bkh),
        Point(u3, bkh),
        Point(u3, 1),
        Point(u1, 1),
        Point(u1, 0)
    ]

    u4 = u2 + keyboard_dimensions.black_key_width
    lookup[Chroma.C_SHARP] = [
        Point(u2, 0),
        Point(u4, 0),
        Point(u4, bkh),
        Point(u2, bkh),
        Point(u2, 0)
    ]

    u6 = 2*keyboard_dimensions.white_key_width
    u5 = u6 - keyboard_dimensions.black_key_width/2 + keyboard_dimensions.offset_1
    lookup[Chroma.D] = [
        Point(u4, 0),
        Point(u5, 0),
        Point(u5, bkh),
        Point(u6, bkh),
        Point(u6, 1),
        Point(u3, 1),
        Point(u3, bkh),
        Point(u4, bkh),
        Point(u4, 0)
    ]

    u7 = u5 + keyboard_dimensions.black_key_width
    lookup[Chroma.D_SHARP] = [
        Point(u5, 0),
        Point(u7, 0),
        Point(u7, bkh),
        Point(u5, bkh),
        Point(u5, 0)
    ]

    u8 = 3*keyboard_dimensions.white_key_width
    lookup[Chroma.E] = [
        Point(u7, 0),
        Point(u8, 0),
        Point(u8, 1),
        Point(u6, 1),
        Point(u6, bkh),
        Point(u7, bkh),
        Point(u7, 0)
    ]

    u10 = 4*keyboard_dimensions.white_key_width
    u9 = u10 - keyboard_dimensions.black_key_width/2 - keyboard_dimensions.offset_2
    lookup[Chroma.F] = [
        Point(u8, 0),
        Point(u9, 0),
        Point(u9, bkh),
        Point(u10, bkh),
        Point(u10, 1),
        Point(u8, 1),
        Point(u8, 0)
    ]

    u11 = u9 + keyboard_dimensions.black_key_width
    lookup[Chroma.F_SHARP] = [
        Point(u9, 0),
        Point(u11, 0),
        Point(u11, bkh),
        Point(u9, bkh),
        Point(u9, 0)
    ]

    u13 = 5*keyboard_dimensions.white_key_width
    u12 = u13 - keyboard_dimensions.black_key_width/2
    lookup[Chroma.G] = [
        Point(u11, 0),
        Point(u12, 0),
        Point(u12, bkh),
        Point(u13, bkh),
        Point(u13, 1),
        Point(u10, 1),
        Point(u10, bkh),
        Point(u11, bkh),
        Point(u11, 0)
    ]

    u14 = u12 + keyboard_dimensions.black_key_width
    lookup[Chroma.G_SHARP] = [
        Point(u12, 0),
        Point(u14, 0),
        Point(u14, bkh),
        Point(u12, bkh),
        Point(u12, 0)
    ]

    u16 = 6*keyboard_dimensions.white_key_width
    u15 = u16 - keyboard_dimensions.black_key_width/2 + keyboard_dimensions.offset_2
    lookup[Chroma.A] = [
        Point(u14, 0),
        Point(u15, 0),
        Point(u15, bkh),
        Point(u16, bkh),
        Point(u16, 1),
        Point(u13, 1),
        Point(u13, bkh),
        Point(u14, bkh),
        Point(u14, 0)
    ]

    u17 = u15 + keyboard_dimensions.black_key_width
    lookup[Chroma.A_SHARP] = [
        Point(u15, 0),
        Point(u17, 0),
        Point(u17, bkh),
        Point(u15, bkh),
        Point(u15, 0)
    ]

    u18 = 7*keyboard_dimensions.white_key_width
    lookup[Chroma.B] = [
        Point(u17, 0),
        Point(u18, 0),
        Point(u18, 1),
        Point(u16, 1),
        Point(u16, bkh),
        Point(u17, bkh),
        Point(u17, 0)
    ]

    return lookup


# TODO: refactor main into small responsibilities:
# global render context with layout in pixels.
# keyboard component takes care of own rendering.
# fretboard component takes care of own rendering.
# choice of notes to highlight in current frame.
def main():
    # Define image size (optimise for given screen).
    image_size = (2220, 1080)  # Phone
    # image_size = (2160, 1620)  # Tablet
    # image_size = (2560, 1600)  # Laptop

    # Create a new surface and context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *image_size)
    context = cairo.Context(surface)

    # Set background colour.
    # white = Colour(1, 1, 1)
    rgb = 0.8
    grey = Colour(rgb, rgb, rgb)
    context.set_source_rgb(*grey)
    context.paint()

    # Set antialiasing mode
    context.set_antialias(cairo.ANTIALIAS_BEST)

    # Set line width and color.
    black = Colour(0, 0, 0)
    black_key_colour = black
    line_width = 3  # TODO: scale with image.
    context.set_line_width(line_width)
    context.set_source_rgb(*black_key_colour)

    # Establish coordinate system transforms.
    # TODO: make padding a ratio of image size not absolute pixels.
    # TODO: enforce aspect ratio limits for keyboard so never squashed.
    padding_horizontal = 200
    padding_vertical = 100
    top_left = Point(padding_horizontal, padding_vertical)
    bottom_right = Point(image_size[0] - padding_horizontal, image_size[1]/2 - padding_vertical)
    normed_to_global = get_transform(top_left, bottom_right)

    # Define keyboard dimensions.
    # TODO: add octave width as dimension or infer?
    # TODO: hide these calculations in the constructor?
    # TODO: capture octave of first C.
    num_octaves=3
    golden_ratio = 2/(1 + math.sqrt(5))
    white_key_width = 1/(7*num_octaves)
    black_key_width = golden_ratio*white_key_width
    keyboard_dimensions = KeyboardDimensions(
        num_octaves=num_octaves,
        white_key_width=white_key_width,
        black_key_width=black_key_width,
        black_key_height=golden_ratio,
        offset_1=black_key_width/6,
        offset_2=black_key_width/4
    )
    
    lookup = get_key_vertices_lookup(keyboard_dimensions)

    # TODO: add offset for octave.
    # TODO: use this for real not just debugging. Move it out of here.
    def draw_key(note: Note, colour: Colour):
        vertices = lookup[note.chroma]
        # print(vertices)
        vertices_global = normed_to_global_list(vertices, normed_to_global)
        draw_polygon(context, vertices_global, colour)
    
    # TODO: why do edges not quite line up?! Because edge colour on outside of polygon? If yes, drop it!
    # TODO: styling of colours defined separately.
    red = Colour(1, 0, 0)
    green = Colour(0, 1, 0)
    blue = Colour(0, 0, 1)
    # draw_key(Note(Chroma.C, 0), blue)
    # draw_key(Chroma.C, blue)
    # draw_key(Chroma.C_SHARP, green)
    # draw_key(Chroma.D, red)
    # draw_key(Chroma.D_SHARP, green)
    # draw_key(Chroma.E, blue)
    # draw_key(Chroma.F, red)
    # draw_key(Chroma.F_SHARP, green)
    # draw_key(Chroma.G, blue)
    # draw_key(Chroma.G_SHARP, green)
    # draw_key(Chroma.A, red)
    # draw_key(Chroma.A_SHARP, green)
    # draw_key(Chroma.B, blue)

    # TODO: library of chords.
    A5 = "577xxx"
    positions = chord_string_to_fretboard_positions(A5)
    tuning = GuitarTuning()
    notes = [tuning.position_to_note(position) for position in positions]
    for note in notes:
        print(note)
        draw_key(note, blue)
    # TODO: draw keys not highlighted in white and grey.
    # (If colour not specified, use defaults).

    # Save the image as PNG
    surface.write_to_png("keyboard.png")


if __name__ == '__main__':
    main()
