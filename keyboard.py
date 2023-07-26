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
Option to print labels on keys, could be note names, scale degrees, fingering.
Encapsulate coordinate transformations in drawing functions.
SVG equivalent (for React).
"""

from dataclasses import dataclass
from enum import Enum
import math
from typing import Dict, List, NamedTuple

import cairo


# TODO: C as 1? (Does it matter?)
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


# TODO: remove?
def is_black_key(pitch: Pitch):
    return pitch in [Pitch.A_SHARP, Pitch.C_SHARP, Pitch.D_SHARP, Pitch.F_SHARP, Pitch.G_SHARP]

# TODO: remove?
def is_white_key(pitch: Pitch):
    return not is_black_key(pitch)


KeyVerticesLookup = Dict[Pitch, List[Point]]

# TODO: define template for each shape then add X offset for octave.
# TODO: also scale in X for number of octaves? (Define keys in x in [0, 1].)
# TODO: separate file?
def get_key_vertices_lookup(keyboard_dimensions: KeyboardDimensions) -> KeyVerticesLookup:
    lookup: KeyVerticesLookup = {}

    bkh = keyboard_dimensions.black_key_height
    
    u1 = 0
    u3 = keyboard_dimensions.white_key_width
    u2 = u3 - keyboard_dimensions.black_key_width/2 - keyboard_dimensions.offset_1
    lookup[Pitch.C] = [
        Point(u1, 0),
        Point(u2, 0),
        Point(u2, bkh),
        Point(u3, bkh),
        Point(u3, 1),
        Point(u1, 1),
        Point(u1, 0)
    ]

    u4 = u2 + keyboard_dimensions.black_key_width
    lookup[Pitch.C_SHARP] = [
        Point(u2, 0),
        Point(u4, 0),
        Point(u4, bkh),
        Point(u2, bkh),
        Point(u2, 0)
    ]

    u6 = 2*keyboard_dimensions.white_key_width
    u5 = u6 - keyboard_dimensions.black_key_width/2 + keyboard_dimensions.offset_1
    lookup[Pitch.D] = [
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
    lookup[Pitch.D_SHARP] = [
        Point(u5, 0),
        Point(u7, 0),
        Point(u7, bkh),
        Point(u5, bkh),
        Point(u5, 0)
    ]

    u8 = 3*keyboard_dimensions.white_key_width
    lookup[Pitch.E] = [
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
    lookup[Pitch.F] = [
        Point(u8, 0),
        Point(u9, 0),
        Point(u9, bkh),
        Point(u10, bkh),
        Point(u10, 1),
        Point(u8, 1),
        Point(u8, 0)
    ]

    u11 = u9 + keyboard_dimensions.black_key_width
    lookup[Pitch.F_SHARP] = [
        Point(u9, 0),
        Point(u11, 0),
        Point(u11, bkh),
        Point(u9, bkh),
        Point(u9, 0)
    ]

    u13 = 5*keyboard_dimensions.white_key_width
    u12 = u13 - keyboard_dimensions.black_key_width/2
    lookup[Pitch.G] = [
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
    lookup[Pitch.G_SHARP] = [
        Point(u12, 0),
        Point(u14, 0),
        Point(u14, bkh),
        Point(u12, bkh),
        Point(u12, 0)
    ]

    u16 = 6*keyboard_dimensions.white_key_width
    u15 = u16 - keyboard_dimensions.black_key_width/2 + keyboard_dimensions.offset_2
    lookup[Pitch.A] = [
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
    lookup[Pitch.A_SHARP] = [
        Point(u15, 0),
        Point(u17, 0),
        Point(u17, bkh),
        Point(u15, bkh),
        Point(u15, 0)
    ]

    u18 = 7*keyboard_dimensions.white_key_width
    lookup[Pitch.B] = [
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
    # TODO: add octave width as dimension or infer?
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
    # note = Note(Pitch.C, octave=0)
    lookup = get_key_vertices_lookup(keyboard_dimensions)

    # TODO: use this for real not just debugging. Move it out of here.
    def draw_key(pitch, colour):
        vertices = lookup[pitch]
        print(vertices)
        tmp = normed_to_global_list(vertices, normed_to_global)
        draw_polygon(context, tmp, colour)
    
    # TODO: why do edges not quite line up?! Because edge colour on outside of polygon? If yes, drop it!
    red = Colour(1, 0, 0)
    green = Colour(0, 1, 0)
    blue = Colour(0, 0, 1)
    draw_key(Pitch.C, blue)
    draw_key(Pitch.C_SHARP, green)
    draw_key(Pitch.D, red)
    draw_key(Pitch.D_SHARP, green)
    draw_key(Pitch.E, blue)
    draw_key(Pitch.F, red)
    draw_key(Pitch.F_SHARP, green)
    draw_key(Pitch.G, blue)
    draw_key(Pitch.G_SHARP, green)
    draw_key(Pitch.A, red)
    draw_key(Pitch.A_SHARP, green)
    draw_key(Pitch.B, blue)

    # Save the image as PNG
    surface.write_to_png("keyboard.png")


if __name__ == '__main__':
    main()
