import * as _ from "underscore"
import * as $ from "jquery"
import * as p from 'core/properties';
import {LayoutDOM, LayoutDOMView} from 'models/layouts/layout_dom';


class MapRendererView extends LayoutDOMView {
  
  constructor(options) {
    console.log('MapRendererView');
    super(options);
    this.render();
  }
  
  render() {
    console.log('render()');
    this.$el.html(`MapRenderer: ${this.model.name}`);
  }
}


export class MapRenderer extends LayoutDOM {}
MapRenderer.prototype.default_view = MapRendererView;
MapRenderer.prototype.type = 'MapRenderer';
