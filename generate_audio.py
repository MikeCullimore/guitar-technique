"""
generate_audio.py

Play with generating audio.

https://stackoverflow.com/questions/48043004/how-do-i-generate-a-sine-wave-using-python

todo:
Add audio to animations: MoviePy.
Save waveform plots.
For chords and sequences of notes, add onset delay between each.
Improve Karplus-Strong implementation.
    Tune parameters to sound guitar-like.
    Timbre of guitar or piano.
    https://flothesof.github.io/Karplus-Strong-algorithm-Python.html (also includes moviepy animation!)
    https://users.soe.ucsc.edu/~karplus/papers/digitar.pdf
    https://introcs.cs.princeton.edu/java/assignments/guitar.html
Add effects e.g. distortion, delay, compression.
Use PyGame? https://www.pygame.org/wiki/about
Listen to samples here: https://freesound.org/search/?q=guitar+string
Play back programmatically.
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

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

from chroma import Chroma
from notes import midi_to_frequency, note_to_midi
from scales import get_major_triad

# fs = 8000
fs = 44100  # Sampling frequency [Hz]
folder = 'data'

def karplus_strong(frequency):
    """
    Karplus-Strong string synthesis.

    todo:
    Handle multiple frequencies at this level?
    Animate wavetable modification (becomes travelling sine wave and amplitude decays).
    """
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
    for i in range(num_samples):
        wavetable[current_sample] = 0.5*(wavetable[current_sample] + previous_value)
        signal[i] = wavetable[current_sample]
        previous_value = signal[i]
        current_sample = (current_sample + 1) % wavetable_size
    
    return signal

def sin(frequency, samples):
    # todo: remove when no longer needed.
    return np.sin(2 * np.pi * frequency * samples)

def save_wav(signal, filename='tmp.wav'):
    """Save to WAV file."""
    filepath = os.path.join(folder, filename)
    wavfile.write(filepath, fs, signal)

def main_harmonics():
    duration = 1  # [s]
    samples = np.arange(duration * fs) / fs
    
    # Construct signal.
    # chromas = [Chroma.C]
    chromas = get_major_triad(Chroma.C)
    octave = 4  # todo: what if notes not all in same octave? Handle in scales.py.
    signal = np.zeros(len(samples))
    for chroma in chromas:
        midi = note_to_midi(chroma, octave)
        frequency = midi_to_frequency(midi)
        # print(f'Frequency [Hz]: {frequency}')
        signal += sin(frequency, samples)
    signal /= len(chromas)  # Normalise.
    signal *= 32767  # Scale to fill WAV file range?
    signal = np.int16(signal)  # todo: set this from the start?

    # Plot.
    plt.figure()
    plt.title('Waveform')
    plt.plot(samples, signal)
    plt.show()

    # Save to WAV file.
    save_wav(signal)

def main_ks():
    """Karplus-Strong, one frequency."""
    # frequency = 55  # From example.
    # frequency = 261.26  # C4
    frequency = 440  # A4
    # duration = 1
    # num_samples = fs*duration + 1
    signal = karplus_strong(frequency)

    plt.figure()
    plt.plot(signal)
    # plt.xlim(0, 1000)
    plt.show()

    # save_wav(signal)

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
    save_wav(signal, 'KS C major triad.wav')

if __name__ == '__main__':
    # main_harmonics()
    # main_ks()
    main_ks2()
