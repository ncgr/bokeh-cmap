import * as _ from "underscore"
import * as $ from "jquery"
import * as p from 'core/properties';
import {LayoutDOM, LayoutDOMView} from 'models/layouts/layout_dom';


class MapSetRendererView extends LayoutDOMView {    

  constructor(options) {
    super(options);
    this.render();
  }
  
  render() {
    console.log('render()');
    this.$el.html(`MapSetRenderer: ${this.model.name}`);
  }
}


export class MapSetRenderer extends LayoutDOM {}
MapSetRenderer.prototype.default_view = MapSetRendererView;
MapSetRenderer.prototype.type = 'MapSetRenderer';
