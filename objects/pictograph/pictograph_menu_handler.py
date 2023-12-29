from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QPoint
from objects.arrow.arrow import Arrow
from objects.graphical_object import GraphicalObject
from objects.prop.prop import Prop
from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QGraphicsItem
if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from objects.pictograph.pictograph import Pictograph


class PictographMenuHandler:
    def __init__(self, main_widget: "MainWidget", pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.main_widget = main_widget
        self.export_handler = main_widget.export_handler

    def create_master_menu(self, event_pos: QPoint, clicked_item) -> None:
        menu = QMenu()

        arrow_menu = menu.addMenu("Arrow")
        # self._add_arrow_actions(arrow_menu, clicked_item)

        prop_menu = menu.addMenu("Prop")
        # self._add_prop_actions(prop_menu, clicked_item)

        pictograph_menu = menu.addMenu("Pictograph")
        # self._add_pictograph_actions(pictograph_menu)
#
        menu.exec(event_pos)


