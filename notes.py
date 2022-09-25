"""
notes.py

todo:
Convert chroma to note names, accounting for key (e.g. is note C# or D♭?).
Convert note and octave to pitch (configurable tuning, start with concert pitch).
Convert note and octave to string and fret numbers, throwing error if out of range.
    If multiple matches, return them all. Separate algorithm to choose which given context of other notes.
"""

from enum import Enum, auto

class Chroma(Enum):
    A = auto()
    A_SHARP = auto()
    B = auto()
    C = auto()
    C_SHARP = auto()
    D = auto()
    D_SHARP = auto()
    E = auto()
    F_SHARP = auto()
    F = auto()
    G = auto()
    G_SHARP = auto()

notes_to_frets = {
    Chroma.A: (0, 0)
}

def main():
    # note = Chroma.C
    # print(note.name)
    # print(note.value)
    # print('♭')
    
    # for c in Chroma:
    #     print(c, c.name, c.value)
    
    x = notes_to_frets[Chroma.A]
    print(x)

if __name__ == '__main__':
    main()
