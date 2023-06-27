"""
todo:

* Formatting (black?).
* Make root note an enum also.
* Default arguments.
* Input validation.
* Type annotations.
* Write method stubs to define structure.
* Why does `python cli.py -h` not show help?
* Provide input as JSON not CLI args?
* setup.py to make this a real CLI
* Design for different types of video:
    * Ear trainer: intervals, chords
    * Guitar scales
    * Piano scales
    * Playing along to a song
    * Draw a design and upload image to repo.
"""

import argparse
from enum import Enum
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

class ScaleType(Enum):
    MAJOR = 1
    MINOR = 2


def make_video(scale_type, root, bpm):
    midi = make_midi(scale_type, root, bpm)
    make_animation(midi)
    make_audio(midi)


def make_midi(scale_type, root, bpm):
    pass


def make_animation(midi):
    # for time, notes in midi:
    # make_animation_frame(notes)
    pass


def make_audio(midi):
    pass


def make_animation_frame(time):
    pass


def synthesise_piano_audio(midi):
    pass


def synthesise_guitar_audio(midi):
    pass


def main():
    logger.info("One day this will be a CLI!")

    parser = argparse.ArgumentParser(
        prog='GuitarTechnique',
        description='Makes videos for guitar technique practise.'
    )

    parser.add_argument('-b', '--bpm', help='Tempo in beats per minute')
    parser.add_argument('-r', '--root', help='Scale root note')
    parser.add_argument('-s', '--scale', help='Scale type: major or minor.')

    args = parser.parse_args()
    bpm = args.bpm
    root = args.root  # TODO: validate
    scale_type = ScaleType(int(args.scale))
    
    logger.info(f'BPM: {bpm}')
    logger.info(f'Root note: {root}')
    logger.info(f'Scale type: {scale_type}')

    make_video(scale_type, root, bpm)


if __name__ == '__main__':
    main()
