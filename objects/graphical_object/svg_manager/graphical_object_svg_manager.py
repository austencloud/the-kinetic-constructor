from typing import Union
from .arrow_svg_manager import ArrowSvgManager
from .prop_svg_manager import PropSvgManager
from .svg_file_manager import SvgFileManager
from .svg_color_manager import SvgColorManager

from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop

class GraphicalObjectSvgManager:
    def __init__(self) -> None:
        self.file_manager = SvgFileManager(self)
        self.color_manager = SvgColorManager(self)
        self.arrow_manager = ArrowSvgManager(self)
        self.prop_manager = PropSvgManager(self)


    def update_svg(self, object: Union["Arrow", "Prop"]) -> None:
        if isinstance(object, Arrow):
            self.arrow_manager.update_arrow_svg(object)
        elif isinstance(object, Prop):
            self.prop_manager.update_prop_svg(object)

    def get_svg_file(self, object: Union["Arrow", "Prop"]) -> str:
        if isinstance(object, Arrow):
            return self.arrow_manager.get_arrow_svg_file(object)
        elif isinstance(object, Prop):
            return self.prop_manager.get_prop_svg_file(object)
