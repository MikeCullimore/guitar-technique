"""
NeckRenderer

Render images of the neck with markers at the given positions.
"""


import os.path

from PIL import Image

class NeckRenderer:
    def __init__(self):
        # Load input images.
        self._folder = 'data'
        self._frets = self._imread('guitar-fretboard.png')
        self._marker = self._imread('circle.png')
        self._marker_width, self._marker_height = self._marker.size

        # Measured positions of fretboard edges and strings.
        self._fret_edges = [140,266,385,497,603,703,797,886,970,1049,1124,1195,1261,1324,1384,1440,1493,1543,1590,1634,1676,1716,1753,1789]
        self._string_centres = [25,53,81,109,137,165]
        self._num_strings = len(self._string_centres)
    
    def render_image(self, positions):
        """Render an image of the neck with markers at the given positions."""
        # Shallow copy: necessary?
        output = self._frets.copy()
        
        for (string, fret) in positions:
            offset = self._calculate_offset(string, fret)
            output.paste(self._marker, offset)
        return output
    
    def render_images(self, sequence):
        """Given a sequence of positions, generate corresponding images.
        
        todo:
        Input validation
        Error handling
        Generator rather than load all images at once.
        """
        images = []
        for positions in sequence:
            image = self.render_image(positions)
            images.append(image)
        return images
    
    def _calculate_offset(self, string, fret):
        """Calculate the (x, y) offset needed to position the marker on a given string and fret.""" 
        x = self._fret_edges[fret - 1] - self._marker_width
        y = self._string_centres[self._num_strings - string] - self._marker_height//2
        return (x, y)
    
    def _imread(self, filename):
        return Image.open(os.path.join(self._folder, filename))
    
    def _imsave(self, image, filename):
        image.save(os.path.join(self._folder, filename))
    