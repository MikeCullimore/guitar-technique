"""
create_video.py

Combine images and audio into single video file.

todo:
Read docs: https://zulko.github.io/moviepy/getting_started/videoclips.html
Better to compose synchronised frames (functions of time) rather than combine existing files?
    AudioArrayClip: directly from array (no intermediate file).
Just add images at specified times e.g. myclip.save_frame("frame.jpeg", t='01:00:00') # frame at time t=1h
Draw the desired end result as a guide: musical score, tab and fretboard stacked vertically.
    Piano variant without the tablature.
Make folder name and get_filepath global?
"""

import os.path

import moviepy.editor as mpy

folder = 'data'

def get_filepath(filename):
    return os.path.join(folder, filename)

def main():
    animation = mpy.VideoFileClip(get_filepath('pentatonic.gif'))
    audio = mpy.AudioFileClip(get_filepath('tmp.wav'))
    video = animation.set_audio(audio)  # Returns a new video clip!
    video.write_videofile(get_filepath('tmp.webm'))

if __name__ == '__main__':
    main()
