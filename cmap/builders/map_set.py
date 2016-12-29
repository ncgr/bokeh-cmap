'''
MapSetBuilder: Build a Map Set from a dataframe.
'''
import os
from cmap.builders.builder import Builder
from cmap.builders.map import MapBuilder


class MapSetBuilder(Builder):
    def __init__(self, *ignore, df, plot):
        self.df = df
        self.plot = plot
        self.selected_map = None
        self.name = None

    def _resolve_map_set_name(self):
        '''
        find the map-set name based on the dataframe source path/url
        '''
        # TODO: if the file was badly named, or fetched from a rest api, then
        # this name might not be descriptive. Instead the first column (map_acc)
        # could be used, e.g. PvConsensus_GaleanoFernandez2011_a_Pv01

        filename = os.path.split(self.df.src)[1]  # path, *filename*
        self.name = os.path.splitext(filename)[0]  # *file*, ext
        print(self.name)

    def build(self):
        self._resolve_map_set_name()
        self.map_dfs = self.df.groupby('map_name')
        self.map_names = [name for name, group in self.map_dfs]
        self.map_builders = [
            MapBuilder(name=name, df=group, plot=self.plot)
            for name, group in self.map_dfs
        ]
        for b in self.map_builders: b.build()

        # TODO: apply selected_map, or select first one
        # TODO: get min/max of all features for current map selection
        # TODO: render map set as a select widget on our Figure
