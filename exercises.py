"""
Guitar exercises: structured practice sessions.
"""

import random

from notes import chroma_list

string_names = ['low E', 'A', 'D', 'G', 'B', 'high E']
open_chords = ['C', 'D', 'F', 'Am']  # todo: add all those listed in brown notebook.
keys = ['C', 'G', 'D', 'A', 'E', 'B/C♭', 'G♭/F#', 'D♭/C#', 'A♭', 'E♭', 'B♭', 'F', 'a', 'e', 'b', 'f#', 'c#', 'g#', 'e♭/d#', 'b♭', 'f', 'c', 'g', 'd']

def random_chroma():
    """Choose a random chroma value."""
    return random.choice(chroma_list).name

def random_string():
    """Choose a random string."""
    return random.choice(string_names)

def random_open_chord():
    """Choose a random open chord."""
    return random.choice(open_chords)

def random_key():
    """Choose a random key."""
    return random.choice(keys)

def main():
    # todo: option to go round again?
    # todo: option to skip an exercise?
    # todo: select random subset (once list gets too long)?
    # todo: pair with image/animation.
    # todo: chords: loop a list (say four chords?).
    exercises = [
        f'Play every {random_chroma()} on the neck.',
        f'Play a chromatic scale along the {random_string()} string.',
        f'Play a {random_chroma()} minor pentatonic scale.',
        f'Play a {random_chroma()} minor scale.',
        f'Play a {random_chroma()} major scale.',
        f'Play a {random_open_chord()} open chord.',
        f'Play all the arpeggios in the key of {random_key()}.'  # todo: explain what they are!
    ]
    random.shuffle(exercises)

    for exercise in exercises:
        print(exercise)
        input('Press enter to continue...')
    print('Well done! Session complete!')

if __name__ == '__main__':
    main()
