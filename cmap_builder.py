#!/usr/bin/env python

"""
cmap_builder

to view help & options, run: map_builder --help
"""
import argparse

from bokeh.io import show
from bokeh.plotting import Figure, curdoc
from bokeh.layouts import gridplot
from bokeh.models import GlyphRenderer
from bokeh.models.sources import ColumnDataSource
from cmap.builders.loader import Loader
from cmap.builders.map_set import MapSetBuilder


TOOLS = 'resize,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select'
GRID_COLS = 12

def main():
    parser = setup_argparse()
    args = parser.parse_args()
    data_frames = [Loader(src).load_dataframe() for src in args.src_files]
    map_set_builders = [ MapSetBuilder(df=df) for df in data_frames ]
    plots = [b.build() for b in map_set_builders]
    # TODO: here all the maps are being flattened, ignoring MapSets. Give user some selection 
    # for what Map(s) to display
    plots = [plot for sublist in plots for plot in sublist]  # flatten lists
    grid = gridplot(plots, ncols=GRID_COLS)
    show(grid)

def setup_argparse():
    """
    Configure and return the argparser for command line options and help.
    """
    parser = argparse.ArgumentParser(
        description='CMAP builder',
        epilog='are all the CMAP builder options!'
    )
    parser.add_argument(
        'src_files',
        nargs='+',
        help="One or more CMAP or GFF delimited text files or remote URLs."
    )
    return parser


if __name__ == '__main__':
    main()
