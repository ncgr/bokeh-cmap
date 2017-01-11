"""
MapSpine is a subclass Quad and QuadView
"""

from os import path
from bokeh.models.glyphs import Quad
from bokeh.util.compiler import FromFile

script_path = path.dirname(path.abspath( __file__ ))

class MapSpine(Quad):

    __implementation__ = FromFile(script_path + '/map_spine.js')

    def __init__(self, **kwargs):
        Quad.__init__(self, **kwargs)
