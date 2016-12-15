import numpy as np
import pandas as pd

from bokeh.io import show
from bokeh.plotting import Figure
from bokeh.models import Label, GlyphRenderer
from bokeh.models.sources import ColumnDataSource

from models.map_spine import MapSpine

TOOLS = 'resize,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select'
plot = Figure(tools=TOOLS)
plot.xaxis.visible = False
plot.yaxis.visible = False

data_source = ColumnDataSource(data={})
spine = MapSpine(x=10, y=10, width=1, height=20)
spine2 = MapSpine(x=50, y=10, width=1, height=30)
glyph_renderer = GlyphRenderer(glyph=spine, data_source=data_source)
glyph_renderer2 = GlyphRenderer(glyph=spine2, data_source=data_source)

plot.add_layout(glyph_renderer)
plot.add_layout(glyph_renderer2)

show(plot)
