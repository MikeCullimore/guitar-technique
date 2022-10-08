"""
notes.py

Conversion between note (chroma and octave), MIDI number, piano key number, frequency.

todo:
Note as struct (chroma and octave).
Add a frequency conversion function which accounts for string inharmonicity (see Railsback curve).
"""

from chroma import chroma_list, len_chroma

MIDI_MIN = 0
MIDI_MAX = 128
PIANO_MIN = 1
PIANO_MAX = 88
MIDI_A4 = 69
A4_FREQUENCY = 440  # [Hz]

def midi_to_piano(midi):
    """Convert MIDI note number to piano key number."""
    if midi < 21:
        raise ValueError('MIDI note number must be greater than or equal to 21.')
    
    if midi > 108:
        raise ValueError('MIDI note number must be less than or equal to 108.')
    
    return midi - 20

def piano_to_midi(piano):
    """Convert piano key number to MIDI note number."""
    if piano < PIANO_MIN:
        raise ValueError(f'Piano key number must be greater than or equal to {PIANO_MIN}.')
    
    if piano > PIANO_MAX:
        raise ValueError(f'Piano key number must be less than or equal to {PIANO_MAX}.')
    
    return piano + 20

def midi_to_note(midi):
    """Convert MIDI note number to note (chroma, octave)."""
    chroma_index = midi % len_chroma
    chroma = chroma_list[chroma_index]
    octave = (midi // len_chroma) - 1
    # print(f'MIDI: {midi}, chroma: {chroma}, octave: {octave}')
    return (chroma, octave)

def note_to_midi(chroma, octave):
    """Convert note (chroma, octave) to MIDI note number."""
    chroma_index = chroma_list.index(chroma)
    return (octave + 1)*len_chroma + chroma_index

def midi_to_frequency(midi):
    return A4_FREQUENCY*2**((midi - MIDI_A4)/len_chroma)

def note_to_frequency(chroma, octave):
    return midi_to_frequency(note_to_midi(chroma, octave))

def main():
    midi = 21
    piano = midi_to_piano(midi)
    print(f'MIDI {midi} = piano {piano}')

    piano = 69
    midi = piano_to_midi(piano)
    print(f'Piano {piano} = MIDI {midi}')

    for piano in range(1, PIANO_MAX+1):
        midi = piano_to_midi(piano)
        # chroma, octave = midi_to_note(midi)
        # midi2 = note_to_midi(chroma, octave)
        # print(f'{midi}, {midi2}')
        frequency = midi_to_frequency(midi)
        print(f'MIDI: {midi}, frequency {frequency:.2f}')

if __name__ == '__main__':
    main()
