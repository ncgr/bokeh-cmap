from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc
from bokeh.models.glyphs import Rect, Line
from bokeh.models import (BasicTicker, ColumnDataSource, Grid, LinearAxis,
                         DataRange1d, PanTool, Plot, WheelZoomTool)
from cmap.builders.builder import Builder
from cmap.models.map_spine import MapSpine


class MapBuilder(Builder):
    """
    MapBuilder: build a Map from a dataframe. Each Map is rendered in a separate
    Bokeh Figure.
    """
    TOOLS = 'pan,wheel_zoom,box_zoom,reset,save'
    MAP_WIDTH = 10
    PLOT_WIDTH = 100

    def __init__(self, df, name, map_set_name):
        self.df = df
        self.name = name
        self.map_set_name = map_set_name

    def _check(self):
        map_count = len(self.df.groupby('map_name'))
        assert map_count == 1, 'dataframe consists of more than 1 map_name'

    def build(self):
        self._check()
        # find the min and max
        self.min = self.df['map_start'].min()
        self.max = self.df['map_stop'].max()
        assert self.min <= self.max, 'map_start should be less than map_stop'
        # create a new plot for this map and add to bokeh current doc.
        self.plot = figure(
            title=self.name,
            tools=self.TOOLS,
            width=self.PLOT_WIDTH
        )
        self.plot.yaxis.axis_label = 'cM'
        self.plot.xaxis.visible = False
        self.plot.xgrid.visible = False
        self._build_spine()
        self._build_feature_glyphs()
        self._build_feature_labels()
        return self.plot

    def _build_feature_glyphs(self):
        def _build_feature(rec):
            # FIXME: if start and stop a different, this will draw a sloped
            # line which is incorrect. Instead make a newsublass of Quad?
            y = rec['feature_start']
            x = [0,self.MAP_WIDTH]
            self.plot.line(x=x, y=y, line_color='blue', line_width=2)
            #self.plot.add_glyph(ds, line)
        self.df.apply(_build_feature, axis=1)


    def _build_feature_labels(self):
        pass

    def _build_spine(self):
        d = dict(top=[self.max], bottom=[self.min], left=[0], right=[self.MAP_WIDTH])
        ds = ColumnDataSource(d)
        self.spine = MapSpine(
            top='top', bottom='bottom', left='left', right='right',
            fill_color='#eeeeee'
        )
        self.plot.add_glyph(ds, self.spine)
