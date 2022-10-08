"""
lilypond.py

http://lilypond.org/text-input.html

todo:
Use tablature.
Synchronise with guitar neck images and animate.
    For longer pieces, scroll horizontally.
    Highlight current note(s) in different colour?
Fix PNG output.
    Works when calling lilypond directly at the command line.
    Fails even when input file is in current folder.
    Fails with both os.system and subprocess.run.
    Convert a working format (PDF, SVG) to PNG by another means?
        GIMP? https://www.gimp.org/docs/python/index.html
        Could also be useful for other image manipulation tasks later on (e.g. compositing frames).
    Example error:
        GNU LilyPond 2.22.2
        Processing `data/test.ly'
        Parsing...
        Interpreting music...
        Preprocessing graphical objects...
        Finding the ideal number of pages...
        Fitting music on 1 page...
        Drawing systems...
        Converting to PNG...
        warning: `(gs -q -dNODISPLAY -dNOSAFER -dNOPAUSE -dBATCH -dAutoRotatePages=/None -dPrinted=false /tmp/lilypond-tmp-830687)' failed (32512)
Use abjad or just create text input directly? https://pypi.org/project/abjad/
"""

import inspect
import os.path
import subprocess

def notes():
    # Save Lilypond input to file.
    text = inspect.cleandoc("""
        \\version "2.22.2"
        {    
            c' e' g' e'
        }""")
    # filepath = 'test.ly'
    folder = 'data'
    filepath = os.path.join(folder, 'test.ly')
    with open(filepath, 'w') as f:
        f.write(text)
    
    # Pass file to Lilypond with desired args.
    format = 'svg'  # works
    # format = 'png'  # fails
    commands = ['lilypond', f'--format={format}', f'--output={folder}', filepath]
    completed_process = subprocess.run(commands)
    print(completed_process.stdout)
    print(completed_process.stderr)

def main():
    notes()

if __name__ == '__main__':
    main()
