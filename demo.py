import petl as etl
import random

from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, LabelSet, Label, PrintfTickFormatter
from bokeh.models import HoverTool
from bokeh.models.widgets import Select
from bokeh.models import HoverTool
from bokeh.palettes import brewer
from bokeh.layouts import widgetbox
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.client import push_session

SOURCES = [
    {
        'name' : 'Soybean-GmComposite2003',
        'taxon' : 'Glycine max',
        'path' :  'data/Soybean-GmComposite2003.cmap.txt',
        'label_align' : 'right',
    },
    {
        'name' : 'Soybean-GmConsensus40',
        'taxon' : 'Glycine max',
        'path' :  'data/Soybean-GmConsensus40.cmap.txt',
        'label_align' : 'left',
    }
]
TITLE = 'CMAP-Bokeh'
MAP_NAME = 'K'
X_RANGE = [0,100]
Y_RANGE = [120,-20]
SKEL_WIDTH = 2
X_OFFSET_START = 20
PLOT_WIDTH = 800
PLOT_HEIGHT = 600
INTER_MAP= 30
TOOLS='box_select,lasso_select,poly_select,pan,xpan,ypan,resize,'+ \
      'tap,box_zoom,wheel_zoom,xwheel_zoom,ywheel_zoom,undo,redo,reset,'+ \
      'save,hover'  # exc. crosshair
COLORS = brewer['Spectral'][8];

data_models = []  # list of data models corresponding to the SOURCES list
feature_occurences = dict()  # global occurences of features
feature_aliases = dict()     # global aliases of feature names
singleton_features = dict()
shared_features = dict()
map_names = dict()           # global map names across all sources
sel_map_name = MAP_NAME      # current map name
p = None  # bokeh plot
connector_lines_dc = None
map_labels_dc = None

def main():
    """
    Setup connection to bokeh server, and show our layout.
    """
    load_sources()
    update_data_models()
    update_data_sources()
    curdoc().title = TITLE
    session = push_session(curdoc())
    layout = setup()
    curdoc().add_root(layout)
    session.show(layout)
    session.loop_until_closed()


def load_sources():
    """
    Create data_models for each of SOURCES
    """
    global map_names

    for map_idx, src in enumerate(SOURCES):
        table = etl.io.csv.fromtsv(src['path'])
        data_models.append({ 'table' : table })
    map_names = get_map_names()

def update_data_models():
    """
    Update the data_models having recordsets filtered by selected map name.
    """
    global feature_occurences, singleton_features, shared_features

    feature_occurences = dict()
    singleton_features = dict()
    shared_features = dict()

    for model_idx, model in enumerate(data_models):
        table = model['table']
        model['map_name_selection'] = etl.transform.selects.select(
            table,
            lambda rec: rec.map_name == sel_map_name
        )
        model['features_selection'] = etl.transform.selects.select(
            model['map_name_selection'],
            lambda rec: rec.feature_start == rec.feature_stop
        )
        model['regions_selection'] = etl.transform.selects.select(
            model['map_name_selection'],
            lambda rec: rec.feature_start != rec.feature_stop
        )
        # Update dict of occurences of each feature name in the recordset,
        # matching the current.
        selection = model['features_selection']
        recs = selection.records()
        for rec in selection.records():
            features = feature_occurences.get(rec.feature_name, [])
            features.append(dict(
                map_num=model_idx,
                rec=rec
            ))
            feature_occurences[rec.feature_name] = features

    singleton_features = {
        k: True for k,v in feature_occurences.items() if len(v) == 1
    }
    shared_features = {
        k: True for k,v in feature_occurences.items() if len(v) > 1
    }


def update_data_sources():
    y_range_start = float('inf')
    y_range_stop = float('-inf')

    for map_idx, model in enumerate(data_models):
        sel = model['features_selection']
        recs = sel.records()

        xoffset = X_OFFSET_START + map_idx * INTER_MAP
        #
        # data source for rectangle representing the skeleton of each map.
        #
        map_start = float(recs[0].map_start)
        map_stop = float(recs[0].map_stop)

        if(map_start < y_range_start):
            y_range_start = map_start
        if(map_stop > y_range_stop):
            y_range_stop = map_stop
        d = dict(
            left=   [xoffset],
            right=  [xoffset + SKEL_WIDTH],
            top=    [recs[0].map_start],
            bottom= [recs[0].map_stop],
            color=  [ random.choice(COLORS) ],
            legend= SOURCES[map_idx]['name']
        )
        if(model.get('map_skel_rec_dc')):
            model['map_skel_rec_dc'].data = d;
        else:
            model['map_skel_rec_dc'] = ColumnDataSource(data=d)
        #
        # singleton hash marks
        #
        my_singleton_features = [
            rec for rec in sel.records()
            if singleton_features.get(rec.feature_name)
        ]
        singleton_x = [
            [xoffset, xoffset + SKEL_WIDTH]
            for d in my_singleton_features
        ]
        singleton_y = [
            [d.feature_start, d.feature_start]
            for d in my_singleton_features
        ]
        d = dict(
            x=singleton_x,
            y=singleton_y
        )
        if(model.get('singleton_hash_marks_dc')):
            model['singleton_hash_marks_dc'].data = d;
        else:
            model['singleton_hash_marks_dc'] = ColumnDataSource(data=d)
        #
        # hash marks for each common/shared feature
        #
        my_shared_features = [
            rec for rec in sel.records()
            if shared_features.get(rec.feature_name)
        ]
        shared_x = [
            [xoffset, xoffset + SKEL_WIDTH]
            for d in my_shared_features
        ]
        shared_y = [
            [d.feature_start, d.feature_start]
            for d in my_shared_features
        ]
        d = dict(
            x=shared_x,
            y=shared_y
        )
        if(model.get('shared_hash_marks_dc')):
            model['shared_hash_marks_dc'].data = d;
        else:
            model['shared_hash_marks_dc'] = ColumnDataSource(data=d)
        #
        # labels for common/shared features
        #
        label_align = SOURCES[map_idx]['label_align']
        if label_align == 'left': # left aligned, right side of layout
            label_xoffset = SKEL_WIDTH + 7
        else: # right aligned, left side of layout
            label_xoffset = -7
        d = dict(
            x=           [ xoffset + label_xoffset for i in range(0, len(my_shared_features))],
            y=           [ rec.feature_start for rec in my_shared_features],
            name=        [ rec.feature_name for rec in my_shared_features ],
        )
        if(model.get('shared_labels_dc')):
            model['shared_labels_dc'].data = d;
        else:
            model['shared_labels_dc'] = ColumnDataSource(d)

    #
    # draw connections between the shared occurrences
    #
    global connector_lines_dc
    map1_all_features = data_models[0]['features_selection'].records()
    map1_shared_features = {
        rec.feature_name : rec.feature_start for rec in map1_all_features
        if shared_features.get(rec.feature_name)
    }
    map2_all_features = data_models[1]['features_selection'].records()
    map2_shared_features = {
        rec.feature_name : rec.feature_start for rec in map2_all_features
        if shared_features.get(rec.feature_name)
    }
    x =  [
        [X_OFFSET_START + 0 * INTER_MAP + SKEL_WIDTH,
         X_OFFSET_START + 1 * INTER_MAP]
        for i in range(0, len(shared_features))
    ]
    y = [
        [ map1_shared_features[k], map2_shared_features[k] ]
        for k,v in shared_features.items()
    ]
    d = dict( x=x, y=y )
    if(connector_lines_dc):
        connector_lines_dc.data=d
    else:
        connector_lines_dc = ColumnDataSource(data=d)

    #
    # labels for each map set
    #
    global map_labels_dc
    d = dict(
        x= [
            X_OFFSET_START + i * INTER_MAP + SKEL_WIDTH
            for i in range(0, 2)
        ],
        text= [
            'Map: {0} [{1} features]'.format(
                sel_map_name,
                len(data_models[i]['map_name_selection'])
            )
            for i in range(0,2)
        ]
    )
    if(map_labels_dc):
        map_labels_dc.data=d
    else:
        map_labels_dc = ColumnDataSource(data=d)

    #
    # update the plot y_range
    #
    global p
    if p:
        p.y_range.start = y_range_stop + 10
        p.y_range.end = y_range_start - 20

def get_map_names():
    """
    Build hash with keys having all map names across all tables
    """
    res = dict()
    for model_idx, model in enumerate(data_models):
        table = model['table']
        for rec in table.records():
            res[rec['map_name']] = True
    return res


def on_map_name(attr, old_name, new_name):
    """
    Update all the datasources with the new selected map name.
    """
    global sel_map_name
    sel_map_name = new_name
    update_data_models()
    update_data_sources()


def setup():
    """
    Create vis components, and setup datasources for each.
    """
    x_offset = X_OFFSET_START
    global p
    p = figure(
        plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, responsive=True,
        title=TITLE, toolbar_location='above', x_range=X_RANGE, y_range=Y_RANGE,
        tools=TOOLS
    )
    p.xaxis.visible = False
    p.yaxis.axis_label = 'Centi-morgan'
    p.yaxis[0].formatter = PrintfTickFormatter(format="%4.1f cM")
    p.xgrid.grid_line_color = None

    hover = p.select_one(HoverTool)
    hover.tooltips = [
        ('Name', '@name'),
        ('Position', '@y cM')
    ]
    hover.line_policy = 'nearest'

    # feature_occurences = get_feature_occurences()
    for map_idx, src in enumerate(SOURCES):
        name = src['name']
        taxon = src['taxon']
        path = src['path']
        label_align = src['label_align']
        model = data_models[map_idx]
        recs = model['features_selection'].records();

        # rectangle representing the skeleton of each map.
        p.quad(
            'left', 'right', 'top', 'bottom',
            source=model['map_skel_rec_dc'],
            color='color',
            legend=SOURCES[map_idx]['name']
        )
        # singleton hash marks
        # Note: Hover tool not implemented for multi_line models
        p.multi_line('x', 'y', source=model['singleton_hash_marks_dc'],
            line_color='grey')

        # hash marks for each common/shared feature
        # Note: Hover tool not implemented for multi_line models
        p.multi_line('x', 'y', source=model['shared_hash_marks_dc'],
            line_color='black')

        # add labels for common/shared features
        labels = LabelSet(
            source=model['shared_labels_dc'],
            render_mode='canvas', x='x', y='y', text='name', level='glyph',
            text_color='#666666', text_font_size='10px', text_baseline='middle',
            text_align='center'
        )
        p.add_layout(labels)

        # add some captions, with mapset and other info
        l = Label(x= x_offset, y=-12,
            text=name, render_mode='canvas', text_align='center',
            text_font_size='12px'
        )
        p.add_layout(l)

        l = Label(x= x_offset, y=-9,
            text=taxon, render_mode='canvas', text_align='center',
            text_font_size='10px'
        )
        p.add_layout(l)

        x_offset += INTER_MAP

    map_labels = LabelSet(x='x', y=-6, text='text',
        source=map_labels_dc,
        render_mode='canvas', text_align='center',
        text_font_size='10px'
    )
    p.add_layout(map_labels)

    # last, draw connections between the shared occurrences
    # Note: Hover tool not implemented for multi_line models
    p.multi_line('x', 'y', source=connector_lines_dc)

    # setup select box for map name selection
    opts = sorted([ (n,n) for n in map_names ])
    select = Select(title='Select map name', options=opts, value=sel_map_name)
    select.on_change('value', on_map_name)

    # create simple vertical layout
    layout = column(widgetbox(select), p)
    return layout

if __name__ == '__main__':
    main()
