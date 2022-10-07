"""
metronome.py

Experimenting with metronome using link below.

https://stackoverflow.com/questions/51389691/how-can-i-do-a-precise-metronome

Easier and cleaner to insert into videos instead?
"""

from time import sleep, perf_counter

def main():
    delay = d = 0.2
    print(60 / delay, 'bpm')
    prev = perf_counter()
    for i in range(20):
        sleep(d)
        t = perf_counter()
        delta = t - prev - delay
        print('{:+.9f}'.format(delta))
        d -= delta
        prev = t

if __name__ == '__main__':
    main()
