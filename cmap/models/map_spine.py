"""
MapSpine is just a test of creating a subclass of Glyph and GlyphView
"""

from os import path
from bokeh.models.glyphs import Rect
from bokeh.util.compiler import FromFile

script_path = path.dirname(path.abspath( __file__ ))

class MapSpine(Rect):

    __implementation__ = FromFile(script_path + '/map_spine.js')

    def __init__(self, **kwargs):
        Rect.__init__(self, **kwargs)
