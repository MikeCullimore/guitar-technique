"""
generate_audio.py

Play with generating audio.

https://stackoverflow.com/questions/48043004/how-do-i-generate-a-sine-wave-using-python

todo:
Add audio to animations: MoviePy. See create_video.py.
Save waveform plots.
For chords and sequences of notes, add onset delay between each.
    Reverse delay order for upstrokes.
Improve Karplus-Strong implementation.
    Add stretch factor? Other ways of extending initial noisy transient?
    Improve understanding of how it works: animate wavetable modification.
        See also first-order low pass filters: https://en.wikipedia.org/wiki/Low-pass_filter#First_order
    Tune parameters to sound guitar-like.
        Replace equal weighting of current and previous sample with a, 1-a.
        Simulate guitar body resonance with low-pass filters.
    Timbre of guitar or piano.
    These links have (1) chords (2) better sound (via more parameters) (3) [random] delay between each string, reversed for upstrokes
    http://amid.fish/javascript-karplus-strong
        https://github.com/mrahtz/javascript-karplus-strong
        http://amid.fish/karplus-strong
    
    https://flothesof.github.io/Karplus-Strong-algorithm-Python.html (also includes moviepy animation!)
    https://users.soe.ucsc.edu/~karplus/papers/digitar.pdf
    https://introcs.cs.princeton.edu/java/assignments/guitar.html
Add effects e.g. distortion, delay, compression.
Use PyGame? https://www.pygame.org/wiki/about
Listen to samples here: https://freesound.org/search/?q=guitar+string
Play back programmatically:
    aplay <filename>.wav
    Works at command line but not via subprocess.run(): why?
    Error: command not found.
    Add aplay to environment path? (usr/bin/aplay) usr/bin is on there.
Stereo spread.
Profile and optimise?
Fix libGL errors:
    libGL error: MESA-LOADER: failed to open radeonsi: /home/mike/anaconda3/lib/python3.9/site-packages/matplotlib/../../../libstdc++.so.6: version `GLIBCXX_3.4.29' not found (required by /usr/lib/x86_64-linux-gnu/GL/default/lib/dri/radeonsi_dri.so) (search paths /usr/lib/x86_64-linux-gnu/GL/default/lib/dri, suffix _dri)
    libGL error: failed to load driver: radeonsi
    libGL error: MESA-LOADER: failed to open radeonsi: /home/mike/anaconda3/lib/python3.9/site-packages/matplotlib/../../../libstdc++.so.6: version `GLIBCXX_3.4.29' not found (required by /usr/lib/x86_64-linux-gnu/GL/default/lib/dri/radeonsi_dri.so) (search paths /usr/lib/x86_64-linux-gnu/GL/default/lib/dri, suffix _dri)
    libGL error: failed to load driver: radeonsi
    libGL error: MESA-LOADER: failed to open swrast: /home/mike/anaconda3/lib/python3.9/site-packages/matplotlib/../../../libstdc++.so.6: version `GLIBCXX_3.4.29' not found (required by /usr/lib/x86_64-linux-gnu/GL/default/lib/dri/swrast_dri.so) (search paths /usr/lib/x86_64-linux-gnu/GL/default/lib/dri, suffix _dri)
    libGL error: failed to load driver: swrast
"""

import os.path
import subprocess

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

from chroma import Chroma
from notes import midi_to_frequency, note_to_midi
from scales import get_major_triad

# fs = 8000
fs = 44100  # Sampling frequency [Hz]
folder = 'data'

def karplus_strong(frequency, smoothing_factor=0.5):
    """
    Karplus-Strong string synthesis.

    todo:
    Handle multiple frequencies at this level?
    Animate wavetable modification (becomes travelling sine wave and amplitude decays).
    """
    if (smoothing_factor < 0) or (smoothing_factor > 1):
        raise ValueError(f'smoothing_factor must be in the range [0, 1].')

    # num_samples = np.ceil(duration * fs).astype(int) + 1
    num_samples = 2*fs

    # Initial wavetable: random -1 or 1 (not anywhere in that range!).
    wavetable_size = np.floor(fs/frequency).astype(int)
    wavetable = (2*np.random.randint(0, 2, wavetable_size) - 1).astype(np.float32)

    # plt.figure()
    # plt.plot(wavetable)
    # plt.show()

    signal = np.zeros(num_samples, dtype=np.float32)
    current_sample = 0
    previous_value = 0
    a = smoothing_factor
    b = 1 - smoothing_factor
    for i in range(num_samples):
        wavetable[current_sample] = a*wavetable[current_sample] + b*previous_value
        signal[i] = wavetable[current_sample]
        previous_value = signal[i]
        current_sample = (current_sample + 1) % wavetable_size
    
    return signal

def get_filepath(filename='tmp.wav'):
    return os.path.join(folder, filename)

def save_wav(signal, filepath):
    """Save to WAV file."""
    wavfile.write(filepath, fs, signal)

def play_wav(filepath):
    """Play WAV file."""
    return subprocess.run(['aplay', filepath])

def main_ks():
    """Karplus-Strong, one frequency."""
    # frequency = 55  # From example.
    # frequency = 261.26  # C4
    frequency = 440  # A4
    # duration = 1
    # num_samples = fs*duration + 1
    for sf in [0.3, 0.5, 0.7]:
        signal = karplus_strong(frequency)

        plt.figure()
        plt.title(f'f = {frequency:.0f} Hz, sf = {sf:.1f}')
        plt.plot(signal)
        # plt.xlim(0, 1000)
        plt.show()

        # Save to WAV file.
        filename = f'Karplus-Strong f={frequency:.0f} Hz 10sf={10*sf:.0f}.wav'
        filepath = get_filepath(filename)
        save_wav(signal, filepath)
        
        # play_wav(filepath)

def main_ks2():
    """Karplus-Strong, multiple frequencies.
    
    todo:
    Ensure smooth fade-out at end of array?
    Why do signals not end at zero? Bug? Do they in example?
    """
    # Choose frequencies.
    chromas = get_major_triad(Chroma.C)
    octave = 4  # todo: what if notes not all in same octave? Handle in scales.py.
    frequencies = [midi_to_frequency(note_to_midi(c, octave)) for c in chromas]

    # Construct signal.
    signal = np.zeros(2*fs, dtype=np.float32)
    # plt.figure()
    for frequency in frequencies:
        signal += karplus_strong(frequency)
    #     plt.plot(signal, label=f'{frequency:.0f} Hz')
    # plt.legend()
    # plt.show()
    signal /= len(chromas)  # Normalise. How best?

    # Plot.
    plt.figure()
    plt.title('Waveform')
    plt.plot(signal)
    plt.show()

    # Save to WAV file.
    filename = 'KS C major triad.wav'
    filepath = get_filepath(filename)
    save_wav(signal, filepath)

if __name__ == '__main__':
    main_ks()
    # main_ks2()
