from .arrow_svg_manager import ArrowSvgManager
from .prop_svg_manager import PropSvgManager
from .svg_file_manager import SvgFileManager
from .svg_color_manager import SvgColorManager



class GraphicalObjectSvgManager:
    def __init__(self) -> None:
        self.file_manager = SvgFileManager(self)
        self.color_manager = SvgColorManager(self)
        self.arrow_manager = ArrowSvgManager(self)
        self.prop_manager = PropSvgManager(self)


