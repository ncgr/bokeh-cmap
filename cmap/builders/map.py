'''
MapBuilder: build a Map from a dataframe.
'''
from bokeh.models import ColumnDataSource
from cmap.builders.builder import Builder
from cmap.models.map_spine import MapSpine

class MapBuilder(Builder):
    def __init__(self, *ignore, df, name, plot):
        self.df = df
        self.name = name
        self.plot = plot

    def _check(self):
        map_count = len(self.df.groupby('map_name'))
        assert map_count == 1, 'dataframe consists of more than 1 map_name'

    def build(self):
        self._check()
        # find the min and max
        self.min = self.df['map_start'].min()
        self.max = self.df['map_stop'].max()
        assert self.min <= self.max, 'map_start should be less than map_stop'
        self.height = self.max - self.min
        d = dict(x=[0], y=[self.min], w=[10], h=[self.height])
        spine_data_source = ColumnDataSource(d)
        #spine = MapSpine(x='x', y='0', height='h')
        #self.plot.add_glyph(spine_data_source, spine)
