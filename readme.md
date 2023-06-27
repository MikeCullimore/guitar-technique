# Guitar technique

Tools to help improve guitar-playing technique and understanding of music theory.

# todo

* Explain how to setup, install, run.
* Add example screenshot (can't embed video in markdown).
* Refactor as per notes in red book 7th June:
    * CLI (argparse).
    * Upload videos to YouTube.
    * Click track audio for MVP (essential to practise with a metronome).
    * Phone view is neck only, tablet/desktop view adds e.g. stave, note name.
    * Small functions:
        * make_video(inputs) -> video (= animation + audio)
        * make_animation(inputs) -> animation
        * make_audio(inputs) -> audio
        * make_midi(scale, tempo) -> midi (use as input to animation, audio to sync)
    * Make practise sessions by combining videos (scales, note finding etc.)
    * Views: guitar fretboard, piano, stave (each will need a renderer).
* Ear trainer: play notes separately (melodic) then together (harmonic), show positions.


## Project goals

* Make technical exercises more fun: turn them into a game.
* Learn to navigate the neck: where are notes? Where are chords?
* Learn chord shapes.
* Learn scales.
* Reduce time to change chords.
* Experiment with web APIs (e.g. web audio).
* Play with data visualisation and analysis.
* Play with interesting tools: Rust, TypeScript, Node/Deno, React, Express, Redux, MongoDB, Go, WebAssembly?

## Setup

To generate music scores you will need to install [GNU Lilypond](lilypond.org).

### Activating the virtual environment

Linux: at bash prompt, from root directory:
```
source venv/bin/activate
```

### Installing dependencies

(After activating the virtual environment)
```
pip install -r requirements.txt
```

## Useful links

* [Spectro](https://github.com/calebj0seph/spectro): real-time FFT visualisation of audio (from file or microphone).
* [fft-js](https://www.npmjs.com/package/fft-js)
* [gensound](https://github.com/Quefumas/gensound)

### Identify chords in audio recordings

* [Chord detector (C++)](https://github.com/adamstark/Chord-Detector-and-Chromagram)
* [Capo](https://supermegaultragroovy.com/2010/09/20/capo-2s-innovation/): Mac app for transcription.