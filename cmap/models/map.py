"""
CMAP Map model. A Map consists of a collection of FeatureLocs which are
locations of Feature instances.
"""
from os import path
from bokeh.model import Model
from bokeh.core.properties import Instance, List
from bokeh.util.compiler import FromFile

script_path = path.dirname(path.abspath( __file__ ))


class Map(Model):    
    __implementation__ = FromFile(script_path + '/map.js')
    # feature_locs = List(Instance(FeatureLocation))
