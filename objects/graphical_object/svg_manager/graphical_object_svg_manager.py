from typing import Union
from .arrow_svg_manager import ArrowSvgManager
from .prop_svg_manager import PropSvgManager
from .svg_cache_manager import SvgCacheManager
from .svg_color_manager import SvgColorManager
from .svg_file_manager import SvgFileManager

from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop

from typing import Union


class GraphicalObjectSvgManager:
    def __init__(self) -> None:
        self.cache_manager = SvgCacheManager(self)
        self.file_manager = SvgFileManager(self)
        self.color_manager = SvgColorManager(self)
        self.arrow_manager = ArrowSvgManager(self)
        self.prop_manager = PropSvgManager(self)
        self.preload_svg_cache()

    def preload_svg_cache(self) -> None:
        self.arrow_manager.preload_svgs()
        self.prop_manager.preload_svgs()

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
