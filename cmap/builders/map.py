from cmap.builders.builder import Builder


class MapBuilder(Builder):
    def __init__(self, *ignore, df, name, plot):
        self.df = df
        self.name = name
        self.plot = plot

    def build(self):
        pass
