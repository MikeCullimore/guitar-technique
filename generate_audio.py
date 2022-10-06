"""
generate_audio.py

Play with generating audio.

https://stackoverflow.com/questions/48043004/how-do-i-generate-a-sine-wave-using-python

todo:
Add audio to animations: MoviePy.
Implement Karplus-Strong.
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

fs = 8000
# fs = 44100  # Sampling frequency [Hz]
folder = 'data'

def ks2(frequency, duration):
    """
    Karplus-Strong, refactor in progress.

    todo:
    Handle multiple frequencies at this level?
    Bug: sounds wrong (too electronic/distorted).
        Implement exactly as per link, then adapt?
        In WAV write method?
    """
    # num_samples = np.ceil(duration * fs).astype(int) + 1
    num_samples = 2*fs
    print(f'Frequency [Hz]: {frequency}')
    print(f'Duration [s]: {duration}')

    # Initial wavetable: random -1 or 1 (not anywhere in that range!).
    dtype = np.int16
    # iinfo = np.iinfo(dtype)
    wavetable_size = np.floor(fs/frequency).astype(int)
    # wavetable = np.random.uniform(-1., 1., wavetable_size)
    wavetable = (2*np.random.randint(0, 2, wavetable_size) - 1).astype(float)

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
    
    # signal *= 32767  # Scale to fill WAV file range? todo: save as float 32 instead?
    
    return signal

def karplus_strong(frequency):
    """
    Karplus-Strong string synthesis.

    todo:
    No need to calculate once amplitude drops below some threshold?
    """
    # chroma = Chroma.C
    # octave = 4
    # midi = note_to_midi(chroma, octave)
    # frequency = midi_to_frequency(midi)
    # print(frequency)

    # todo: one wavetable for all frequencies, just loop?
    # wavetable_size = fs // frequency
    # wavetable_size = np.floor(fs/frequency).astype(int)
    duration = 1  # todo: regardless of frequency? Or pad with zeroes when adding?
    wavetable_size = np.ceil(duration * fs).astype(int)
    print(wavetable_size)
    # wavetable = (2*np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
    # wavetable = np.random.randint(-1, 1, wavetable_size, dtype=float)
    wavetable = np.random.uniform(-1., 1., wavetable_size)

    # todo: pre-allocate array of required size.
    # todo: wrap up with frequency as arg.
    samples = []
    num_samples = 2*fs
    current_sample = 0
    previous_value = 0
    while len(samples) < num_samples:
        wavetable[current_sample] = 0.5*(wavetable[current_sample] + previous_value)
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]  # todo: just use above.
        current_sample = (current_sample + 1) % wavetable.size
    samples = np.array(samples)
    return samples

def sin(frequency, samples):
    # todo: remove when no longer needed.
    return np.sin(2 * np.pi * frequency * samples)

def save_wav(signal, filename='tmp.wav'):
    """Save to WAV file."""
    filepath = os.path.join(folder, filename)
    print(signal[0].dtype)
    wavfile.write(filepath, fs, signal)

def main():
    duration = 1  # [s]
    samples = np.arange(duration * fs) / fs
    
    # Construct signal.
    # todo: timbre of guitar.
    chromas = [Chroma.C]
    # chromas = get_major_triad(Chroma.C)
    octave = 4  # todo: what if notes not all in same octave?
    signal = np.zeros(len(samples))
    # signal = np.zeros(2*len(samples))  # todo: remove this hack for Karplus-Strong.
    for chroma in chromas:
        midi = note_to_midi(chroma, octave)
        frequency = midi_to_frequency(midi)
        print(f'Frequency [Hz]: {frequency}')
        signal += sin(frequency, samples)
        # tmp = karplus_strong(frequency)
        # print(signal.shape)
        # print(tmp.shape)
        # print()
        # signal += tmp
    signal /= len(chromas)  # Normalise.
    signal *= 32767  # Scale to fill WAV file range?
    signal = np.int16(signal)  # todo: set this from the start.

    # Plot.
    plt.figure()
    plt.title('Waveform')
    plt.plot(samples, signal)
    plt.show()

    # Save to WAV file.
    save_wav(signal)

if __name__ == '__main__':
    # main()
    # karplus_strong()
    
    frequency = 55  # From example.
    # frequency = 261.26  # C4
    # frequency = 440
    duration = 1
    # num_samples = fs*duration + 1
    signal = ks2(frequency, duration)

    plt.figure()
    plt.plot(signal)
    # plt.xlim(0, 1000)
    plt.show()

    save_wav(signal)
