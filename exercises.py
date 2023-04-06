"""
Guitar exercises: structured practice sessions.

todo:
E natural minor open position.
"Quasi-chromatic scale": finger positions 1-2-3-4 across all strings.
    Then randomise order.
    Different orders ascending and descending.
    See Rock Guitar Secrets PDF, p15.
Generate image/animation to accompany each exercise.
Option to go round again?
Option to skip an exercise?
Select random subset (once list gets too long)?
Chords: loop a list (say four chords?).
Play a song, guess the key (identify the chords).
Piano equivalent (scales, arpeggios, broken chords, pieces).
"""

import random

from chroma import chroma_list

string_names = ['low E', 'A', 'D', 'G', 'B', 'high E']
open_chords = ['C', 'D', 'F', 'Am']  # todo: add all those listed in brown notebook.
keys = ['C', 'G', 'D', 'A', 'E', 'B/C♭', 'G♭/F#', 'D♭/C#', 'A♭', 'E♭', 'B♭', 'F', 'a', 'e', 'b', 'f#', 'c#', 'g#', 'e♭/d#', 'b♭', 'f', 'c', 'g', 'd']
fingers = [1, 2, 3, 4]
songs = [
    'Automatic Stop',
    'Californication',
    'Come As You Are',
    'Day Tripper',
    'Fly Away',
    'I Bet You Look Good on the Dance Floor',
    'Seven Nation Army',
    'Sunshine of Your Love',
    'When the Sun Goes Down'
]

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

def random_song():
    """Choose a random song."""
    return random.choice(songs)

def random_fingering():
    """Choose a random fingering pattern."""
    random.shuffle(fingers)
    return fingers

def main():
    exercises = [
        f'Play every {random_chroma()} on the neck.',
        f'Play a chromatic scale along the {random_string()} string.',
        f'Play a quasi-chromatic scale with fingering {random_fingering()}.',
        f'Play a {random_chroma()} minor pentatonic scale.',
        f'Play a {random_chroma()} minor scale.',
        f'Play a {random_chroma()} major scale.',
        f'Play a {random_open_chord()} open chord.',
        f'Play all the arpeggios in the key of {random_key()}.',  # todo: explain what they are!
        f'Play {random_song()}.'
    ]
    random.shuffle(exercises)

    for exercise in exercises:
        print(exercise)
        input('Press enter to continue...')
        print()
    print('Well done! Session complete!')

if __name__ == '__main__':
    main()
