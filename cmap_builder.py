'''
cmap_builder

to view help & options, run: map_builder --help
'''
import argparse

from bokeh.io import show
from bokeh.plotting import Figure
from bokeh.models import GlyphRenderer
from bokeh.models.sources import ColumnDataSource

from models.map_spine import MapSpine


def main():
    parser = setup_argparse()
    args = parser.parse_args()

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
        help="One or more CMAP or GFF delimited text files."
    )
    return parser


if __name__ == '__main__':
    main()
