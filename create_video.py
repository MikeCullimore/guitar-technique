"""
create_video.py

Combine images and audio into single video file.

todo:
Read docs: https://zulko.github.io/moviepy/getting_started/videoclips.html
Better to compose synchronised frames (functions of time) rather than combine existing files?
    AudioArrayClip: directly from array (no intermediate file).
Just add images at specified times.
Draw the desired end result as a guide: musical score, tab and fretboard stacked vertically.
    Piano variant without the tablature.
"""

import os.path

import moviepy.editor as mpy

from animations import animate
from generate_audio import bpm_to_onsets, pluck_strings, save_wav
from guitar_tuning import GuitarTuning
from notes import note_to_frequency
from scales import append_reversed_sequence

folder = 'data'

def get_filepath(filename):
    """Prepend folder name.
    
    todo: use same everywhere rather than redefine in each file."""
    return os.path.join(folder, filename)

def combine_existing_files(filename_video, filename_audio, filename_output):
    """Combine animation and audio into a video."""
    animation = mpy.VideoFileClip(get_filepath(filename_video))
    audio = mpy.AudioFileClip(get_filepath(filename_audio))
    video = animation.set_audio(audio)  # Returns a new video clip!
    video.write_videofile(get_filepath(filename_output))

def create_files(positions, bpm, fileroot):
    # Convert to frequencies.
    # todo: accommodate multiple frequencies at any given time.
    tuning = GuitarTuning()
    notes = [tuning.position_to_note(*position[0]) for position in positions]  # hack: see above.
    frequencies = [note_to_frequency(chroma, octave) for (chroma, octave) in notes]
    print(frequencies)

    # Configure timings.
    onsets = bpm_to_onsets(bpm, len(frequencies))

    # Generate audio output.
    output = pluck_strings(frequencies, onsets)
    
    # Save to WAV file.
    filename_audio = fileroot + '.wav'
    save_wav(output, filename_audio)

    # Generate animation.
    # todo: handle padding (black frame?).
    filename_animation = fileroot + '.gif'
    animate(positions, filename_animation, bpm)

    # Combine animation with audio.
    # todo: should be out of sync given audio has padding, animation doesn't. Why not then?
    filename_output = fileroot + '.webm'
    combine_existing_files(filename_animation, filename_audio, filename_output)

def c_major_open_position():
    positions = [
        [(1, 0)],
        [(1, 1)],
        [(1, 3)],
        [(2, 0)],
        [(2, 2)],
        [(2, 3)],
        [(3, 0)],
        [(3, 2)],
        [(3, 3)],
        [(4, 0)],
        [(4, 2)],
        [(5, 0)],
        [(5, 1)],
        [(5, 3)],
        [(6, 0)],
        [(6, 1)],
        [(6, 3)],
    ]

    bpm = 100
    fileroot = 'C major open position'
    create_files(positions, bpm, fileroot)

def pentatonic():
    """E minor pentatonic scale."""
    # todo: use create_video
    # todo: revert to array of arrays to accommodate chords. (Implies array of array of frequencies.)
    # todo: move this shape into separate file; provide getter with root note arg.
    # todo: read from ASCII tab format.
    
    # Define pentatonic scale shape.
    pentatonic_ascending = [
        [(1, 12)],
        [(1, 15)],
        [(2, 12)],
        [(2, 14)],
        [(3, 12)],
        [(3, 14)],
        [(4, 12)],
        [(4, 14)],
        [(5, 12)],
        [(5, 15)],
        [(6, 12)],
        [(6, 15)],
    ]
    positions = append_reversed_sequence(pentatonic_ascending)

    bpm = 100
    fileroot = f'E minor pentatonic scale two octaves first position ascending and descending BPM={bpm:d}'
    create_files(positions, bpm, fileroot)

if __name__ == '__main__':
    # combine_existing_files()

    pentatonic()
    # c_major_open_position()
