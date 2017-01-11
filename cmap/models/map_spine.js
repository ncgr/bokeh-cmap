import {Quad, QuadView} from 'models/glyphs/quad';

class MapSpineView extends QuadView {
}


export class MapSpine extends Quad {
}
MapSpine.prototype.default_view = MapSpineView;
MapSpine.prototype.type = 'MapSpine'; // name of the Python class
