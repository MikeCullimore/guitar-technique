"""
generate_audio.py

Generate audio for guitar.

https://stackoverflow.com/questions/48043004/how-do-i-generate-a-sine-wave-using-python

todo:
Improve tone (sounds like a gamelan!).
Tuning trick in original paper p8 to get closer to desired frequency.
Smooth fade-out at end.
Click track? (Optional?)
Save waveform plots.
For chords and sequences of notes, add onset delay between each.
    Classes Guitar, GuitarString?
    Reverse delay order for upstrokes.
Improve Karplus-Strong implementation.
    Amplitude as arg.
    Stretch factor as per 1983 KS paper. Also blend factor?
    Lift out low pass filter for use elsewhere.
    Tune parameters to sound guitar-like.
        Simulate guitar body resonance with low-pass filters.
    These links have (1) chords (2) better sound (via more parameters) (3) [random] delay between each string, reversed for upstrokes
    http://amid.fish/javascript-karplus-strong
        https://github.com/mrahtz/javascript-karplus-strong
        http://amid.fish/karplus-strong
    Add stretch factor? Other ways of extending initial noisy transient?
    Improve understanding of how it works: animate wavetable modification.
        Plot wavetable and output waveform (vertical line indicating current time) together.
        See also first-order low pass filters: https://en.wikipedia.org/wiki/Low-pass_filter#First_order
    https://flothesof.github.io/Karplus-Strong-algorithm-Python.html (also includes moviepy animation!)
    https://users.soe.ucsc.edu/~karplus/papers/digitar.pdf
    https://introcs.cs.princeton.edu/java/assignments/guitar.html
Add effects e.g. distortion, reverb, delay, compression.
Use PyGame? https://www.pygame.org/wiki/about
Listen to samples here: https://freesound.org/search/?q=guitar+string
Play back programmatically:
    aplay <filename>.wav
    Works at command line but not via subprocess.run(): why?
    Error: command not found.
    Add aplay to environment path? (usr/bin/aplay) usr/bin is on there.
Stereo spread. Example from https://github.com/mrahtz/javascript-karplus-strong/blob/master/karplus-strong/guitarstring_asm.js
    // string.acousticLocation is set individually for each string such that
    // the lowest note has a value of -1 and the highest +1
    var stereoSpread = options.stereoSpread * acousticLocation;
    // for negative stereoSpreads, the note is pushed to the left
    // for positive stereoSpreads, the note is pushed to the right
    var gainL = (1 - stereoSpread) * 0.5;
    var gainR = (1 + stereoSpread) * 0.5;
    for (i = 0; i < targetArrayL.length; i++) {
        targetArrayL[i] = heapFloat32[heapOffsets.targetStart+i] * gainL;
    }
    for (i = 0; i < targetArrayL.length; i++) {
        targetArrayR[i] = heapFloat32[heapOffsets.targetStart+i] * gainR;
    }
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
from neck_renderer import bpm_to_milliseconds
from notes import note_to_frequency
from scales import get_major_triad, minor_pentatonic_scale, notes_str, append_reversed_sequence

# fs = 8000
fs = 44100  # Sampling frequency [Hz]
folder = 'data'

def karplus_strong(frequency, smoothing_factor=0.5):
    """
    Karplus-Strong string synthesis.

    todo:
    Wrap up as class: WavetableGroup? (Nothing guitar specific.)
        Maintains wavetable for each string, combines in single output.
        Automatically remove wavetable when amplitude drops below threshold?
    Ensure amplitude always in range [-1, 1], otherwise will clip.
    Handle multiple frequencies at this level? E.g. by combining wavetables?
    Animate wavetable modification (becomes travelling sine wave and amplitude decays).
    Possible to derive analytic expression for amplitude vs time?
        See paper Karplus and Strong 1983.
        Use to decide window: continue until amplitude below threshold.
    Arg for different initial wavetable options: white noise, +/-1, sine chirp, ...?
    Optimise (numpy? numba? Cython?).
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

    # Generate signal.
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
    
    # Remove DC offset.
    signal -= np.mean(signal)
    
    return signal

def milliseconds_to_index(milliseconds):
    return np.ceil(milliseconds*fs/1000).astype(int)

def get_filepath(filename):
    return os.path.join(folder, filename)

def save_wav(signal, filename='tmp.wav'):
    """Save to WAV file."""
    filepath = get_filepath(filename)
    wavfile.write(filepath, fs, signal)

def play_wav(filepath):
    """Play WAV file."""
    return subprocess.run(['aplay', filepath])

def bpm_to_onsets(bpm, num_beats, padding=100):
    """Convert BPM and number of beats to onset times.
    
    todo:
    Use this to generate images and audio.
    Add a little randomness?
    """
    ms = bpm_to_milliseconds(bpm)
    return np.linspace(0, num_beats*ms, num_beats + 1) + padding

def pluck_strings(frequencies, onsets):
    """Generate signals and combine.
    
    todo:
    Duration (samples) as argument to KS: only generate what we need.
    Accommodate array of frequencies at each onset for chords.
        (Add slight delay between each string?)
    """
    # Initialise output array.
    num_samples = milliseconds_to_index(onsets[-1])
    output = np.zeros(num_samples, dtype=np.float32)

    # Generate signals and combine.
    for onset, frequency in zip(onsets[:-1], frequencies):
        component = karplus_strong(frequency)
        start_index = milliseconds_to_index(onset)
        end_index = np.min([num_samples, start_index + len(component)])
        output[start_index:end_index] += component[:end_index-start_index]
    
    # Debugging: plot output.
    plt.figure()
    plt.plot(output)
    plt.show()
    
    return output

def main_ks():
    """Karplus-Strong, one frequency."""
    # frequency = 27.5  # Lowest note on a piano.
    # frequency = 55  # From example.
    # frequency = 261.26  # C4
    frequency = 440  # A4
    # duration = 1
    # num_samples = fs*duration + 1
    
    # Compare different values of smoothing factor to understand its effect.
    for sf in [0.3, 0.5, 0.7]:
        signal = karplus_strong(frequency, sf)

        plt.figure()
        plt.title(f'f = {frequency:.0f} Hz, sf = {sf:.1f}')
        plt.plot(signal)
        # plt.xlim(0, 1000)
        plt.show()

        # Save to WAV file.
        filename = f'Karplus-Strong f={frequency:.0f} Hz 10sf={10*sf:.0f}.wav'
        save_wav(signal, filename)
        
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
    frequencies = [note_to_frequency(c, octave) for c in chromas]

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
    save_wav(signal, filename)

def pentatonic_scale():
    """
    todo: separate function with args frequencies and onsets, return signal.
    """
    # Define frequencies.
    # todo: span two octaves.
    # todo: do not generate signal more than once for any given frequency? But never same: random seed.
    scale = minor_pentatonic_scale(Chroma.A)
    octaves = [4, 5, 5, 5, 5]  # todo: handle in scales.py.
    frequencies = [note_to_frequency(chroma, octave) for (chroma, octave) in zip(scale, octaves)]
    frequencies = append_reversed_sequence(frequencies, loop=True)

    # Configure timings.
    bpm = 60
    onsets = bpm_to_onsets(bpm, len(frequencies))

    # Generate output.
    output = pluck_strings(frequencies, onsets)
    
    # Save to WAV file.
    filename = f'A minor pentatonic scale ascending and descending BPM={bpm:d}.wav'
    save_wav(output, filename)

if __name__ == '__main__':
    main_ks()
    # main_ks2()
    # pentatonic_scale()
