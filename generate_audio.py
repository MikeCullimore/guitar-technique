"""
generate_audio.py

Play with generating audio.

https://stackoverflow.com/questions/48043004/how-do-i-generate-a-sine-wave-using-python

todo:
Add harmonics.
Adapt the spectrum to make it sound like a guitar.
Add effects e.g. distortion.
"""

import os.path

import numpy as np
from scipy.io import wavfile

def main():
    fs = 44100
    f = 1000  # todo: convert from note.
    t = 0.5

    samples = np.arange(t * fs) / fs
    signal = np.sin(2 * np.pi * f * samples)
    signal *= 32767
    signal = np.int16(signal)

    folder = 'data'
    filename = 'tmp.wav'
    filepath = os.path.join(folder, filename)
    wavfile.write(filepath, fs, signal)

if __name__ == '__main__':
    main()
