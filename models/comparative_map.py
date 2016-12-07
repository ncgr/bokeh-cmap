from os import path
from bokeh.models.layouts import LayoutDOM
from bokeh.core.properties import Instance, List
from bokeh.util.compiler import FromFile 
from models.map_renderer import MapRenderer
from models.map_set_renderer import MapSetRenderer

script_path = path.dirname(path.abspath( __file__ ))


class ComparativeMap(LayoutDOM):
    """
    ComparativeMap is the top level component for visualizing one or more maps.
    """
    __implementation__ = FromFile(script_path + '/comparative_map.js')
    
    map_set_renderers = List(Instance(MapSetRenderer))
    map_renderers = List(Instance(MapRenderer))
    
    def __init__(self, map_sets=[], maps=[], *args, **kwargs):            
        LayoutDOM.__init__(self, **kwargs)
        self.map_set_renderers = map_sets
        self.map_renderers = maps
     
