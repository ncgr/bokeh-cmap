import {Rect, RectView} from 'models/glyphs/rect';


class MapSpineView extends RectView {
}


export class MapSpine extends Rect {}
MapSpine.prototype.default_view = MapSpineView;
MapSpine.prototype.type = 'MapSpine'; // name of the Python class
// MapSpineGlyph.coords([['x', 'y']])
