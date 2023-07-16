"""
Draw images of a piano keyboard with given notes marked.

TODO:
Enum for notes.
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
    Explicitly draw white keys as white so not assuming white background.
Operator overloads for point (add, subtract).
Option to print note names on keys.
    Or scale degrees.
Encapsulate coordinate transformations in drawing functions.
SVG equivalent (for React).
"""

from dataclasses import dataclass
from enum import Enum
import math
from typing import List, NamedTuple

import cairo


class Pitch(Enum):
    A = 1
    A_SHARP = 2
    B = 3
    C = 4
    C_SHARP = 5
    D = 6
    D_SHARP = 7
    E = 8
    F = 9
    F_SHARP = 10
    G = 11
    G_SHARP = 12


# TODO: provide method to get frequency?
class Note(NamedTuple):
    pitch: Pitch
    octave: int


class KeyboardDimensions(NamedTuple):
    white_key_width: float
    black_key_width: float
    black_key_height: float
    offset_1: float  # TODO: better name
    offset_2: float  # TODO: better name


class Colour(NamedTuple):
    red: int
    green: int
    blue: int


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


def is_black_key(pitch: Pitch):
    return pitch in [Pitch.A_SHARP, Pitch.C_SHARP, Pitch.D_SHARP, Pitch.F_SHARP, Pitch.G_SHARP]


def is_white_key(pitch: Pitch):
    return not is_black_key(pitch)


# TODO: get_piano_key_vertices (then use instead of loops below).
def get_piano_key_vertices(note: Note, keyboard_dimensions: KeyboardDimensions) -> List[Point]:
    print(f"Black key? {is_black_key(note.pitch)}")
    print(f"White key? {is_white_key(note.pitch)}")
    return []


# TODO: refactor main into small responsibilities:
# global render context with layout in pixels.
# keyboard positions in normed coords.
# choice of notes to highlight in current frame.
def main():
    # Phone screen dimensions.
    image_width = 2220
    image_height = 1080

    # Tablet screen dimensions.
    # image_width = 2160
    # image_height = 1620

    # Tablet screen dimensions.
    # image_width = 2560
    # image_height = 1600

    # Create a new surface and context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, image_width, image_height)
    context = cairo.Context(surface)

    # Set background colour.
    white = Colour(1, 1, 1)
    rgb = 0.8
    grey = Colour(rgb, rgb, rgb)
    context.set_source_rgb(*grey)
    context.paint()

    # Set antialiasing mode
    context.set_antialias(cairo.ANTIALIAS_BEST)

    # Set line width and color.
    black = Colour(0, 0, 0)
    black_key_colour = black
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
    normed_to_global = get_transform(top_left, bottom_right)

    # Define keyboard dimensions.
    golden_ratio = 2/(1 + math.sqrt(5))
    num_octaves = 3
    num_white_keys = 7*num_octaves
    white_key_width = 1/num_white_keys
    black_key_width = golden_ratio*white_key_width
    # TODO: use this in place of raw values.
    keyboard_dimensions = KeyboardDimensions(
        white_key_width=1/num_white_keys,
        black_key_width=golden_ratio*white_key_width,
        black_key_height=golden_ratio,
        offset_1=black_key_width/6,
        offset_2=black_key_width/4
    )
    
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
        draw_polygon(context, vertices, white, black)
    
    # Draw black keys.
    # TODO: use these to define the shapes of white keys also.
    c = black_key_width/6
    d = black_key_width/4
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
        draw_polygon(context, vertices, black, black)
    
    # Debugging.
    note = Note(Pitch.C, octave=0)
    vertices = get_piano_key_vertices(note, keyboard_dimensions)
    print(vertices)

    # Save the image as PNG
    surface.write_to_png("keyboard.png")


if __name__ == '__main__':
    main()
