from bokeh.core.properties import String, Instance
from bokeh.models import LayoutDOM, Slider
from bokeh.util.compiler import FromFile

class Custom(LayoutDOM):
    __implementation__ = FromFile('custom.ts')
    text = String(default="Custom text")
    slider = Instance(Slider)
