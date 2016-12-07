import * as _ from "underscore"
import * as $ from "jquery"
import * as p from "core/properties"
import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"


export class CustomView extends LayoutDOMView {
  
    constructor(options) {    
      super(options);

      this.render();
      this.listenTo(this.model.slider, 'change', () => this.render());
    }    
    render() {    
      this.$el.html(`<h1>Hello, ${this.model.text}: ${this.model.slider.value}</h1>`);
      this.$('h1').css({ 'color': '#686d8e', 'background-color': '#2a3153' });
    }
}

export class Custom extends LayoutDOM {}

Custom.prototype.default_view = CustomView;
Custom.prototype.type = "Custom";

Custom.define({
  text:   [ p.String ],
  slider: [ p.Any    ]
});
