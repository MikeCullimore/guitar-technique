import argparse
from enum import Enum


class ScaleType(Enum):
    MAJOR = 1
    MINOR = 2


def main():
    print("One day this will be a CLI!")

    parser = argparse.ArgumentParser(
        prog='GuitarTechnique',
        description='Makes videos for guitar technique practise.'
    )

    parser.add_argument('-b', '--bpm', help='Tempo in beats per minute')
    parser.add_argument('-r', '--root', help='Scale root note')
    parser.add_argument('-s', '--scale', help='Scale type: major or minor.')


if __name__ == '__main__':
    main()
