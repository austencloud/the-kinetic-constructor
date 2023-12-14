from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QPoint
from objects.arrow.arrow import Arrow
from objects.prop import Prop
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class PictographMenuHandler:
    def __init__(self, main_widget: "MainWidget", pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.main_widget = main_widget
        self.export_handler = main_widget.export_handler

    def create_master_menu(self, event_pos: QPoint, clicked_item) -> None:
        menu = QMenu()

        arrow_menu = menu.addMenu("Arrow")
        self._add_arrow_actions(arrow_menu, clicked_item)

        prop_menu = menu.addMenu("Prop")
        self._add_prop_actions(prop_menu, clicked_item)

        pictograph_menu = menu.addMenu("Pictograph")
        self._add_pictograph_actions(pictograph_menu)

        menu.exec(event_pos)

    ### PROP ACTIONS ###

    def _add_prop_actions(self, menu: QMenu, clicked_item) -> None:
        prop_present = isinstance(clicked_item, Prop)

        delete_action = QAction("Delete", menu)
        delete_action.setEnabled(prop_present)
        delete_action.triggered.connect(lambda: self._delete_selected_prop())
        menu.addAction(delete_action)

    def _delete_selected_prop(self) -> None:
        selected_items = self.pictograph.selectedItems()
        for item in selected_items:
            if isinstance(item, Prop):
                item.delete()

    ### ARROW ACTIONS ###

    def _add_arrow_actions(self, menu: QMenu, clicked_item) -> None:
        arrow_present = isinstance(clicked_item, Arrow)

        delete_action = QAction("Delete", menu)
        delete_action.setEnabled(arrow_present)
        delete_action.triggered.connect(lambda: self._delete_selected_arrow())
        menu.addAction(delete_action)

    def _delete_selected_arrow(self) -> None:
        selected_items = self.pictograph.selectedItems()
        for item in selected_items:
            if isinstance(item, Arrow):
                item.delete()

    ### GRAPHBOARD ACTIONS ###

    def _add_pictograph_actions(self, menu: QMenu) -> None:
        swap_colors_action = QAction("Swap Colorss", menu)
        menu.addAction(swap_colors_action)
