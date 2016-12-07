import * as _ from "underscore"
import * as $ from "jquery"
import * as p from 'core/properties';
import {LayoutDOM, LayoutDOMView} from 'models/layouts/layout_dom';


class ComparativeMapView extends LayoutDOMView {
  
  constructor(options) {    
    super(options);
    this.render();
  }
  
  render() {
    this.$el.html('ComparativeMap');
    console.log(this.model);
  }
}


export class ComparativeMap extends LayoutDOM {}
ComparativeMap.prototype.default_view = ComparativeMapView;
ComparativeMap.prototype.type = 'ComparativeMap';
ComparativeMap.define({
   map_set_renderers : [p.Array, []],
   map_renderers :     [p.Array, []]
});
