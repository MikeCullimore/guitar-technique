"""
chroma.py

todo:
Differentiate between enharmonic notes e.g. C# and D♭: they do not have the
    same pitch in all tuning systems.
"""

from enum import Enum, auto

class Chroma(Enum):
    C = auto()
    C_SHARP = auto()
    D = auto()
    D_SHARP = auto()
    E = auto()
    F = auto()
    F_SHARP = auto()
    G = auto()
    G_SHARP = auto()
    A = auto()
    A_SHARP = auto()
    B = auto()

chroma_list = list(Chroma)
len_chroma = len(chroma_list)
