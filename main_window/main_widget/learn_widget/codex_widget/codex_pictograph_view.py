from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QMenu
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QCursor, QAction, QContextMenuEvent
from base_widgets.base_pictograph.pictograph_view import PictographView

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class CodexPictographView(PictographView):
    def __init__(self, pictograph: "BasePictograph", codex: "Codex") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.pictograph.view = self
        self.codex = codex
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setStyleSheet("border: 1px solid black;")
        
    ### EVENTS ###

    def contextMenuEvent(self, event: QEvent) -> None:
        if isinstance(event, QContextMenuEvent):
            context_menu = QMenu(self)
            context_menu.addSeparator()
            copy_action = QAction("Copy Dictionary", self)
            copy_action.triggered.connect(self.copy_pictograph_dict)
            context_menu.addAction(copy_action)
            context_menu.exec(QCursor.pos())
        else:
            super().contextMenuEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        settings_manager = self.pictograph.main_widget.main_window.settings_manager
        current_prop_type = settings_manager.global_settings.get_prop_type()

        if self.pictograph.prop_type != current_prop_type:
            settings_manager.global_settings.prop_type_changer.replace_props(
                current_prop_type, self.pictograph
            )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        size = self.calculate_view_size()
        self.setMinimumWidth(size)
        self.setMaximumWidth(size)
        self.setMinimumHeight(size)
        self.setMaximumHeight(size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def calculate_view_size(self) -> int:
        codex_scroll_area_bar_width = self.codex.scroll_area.verticalScrollBar().width()
        calculated_width = int((self.codex.learn_widget.width() // 16)) - (
            codex_scroll_area_bar_width // 6
        )
        view_width = calculated_width
        outer_border_width = max(1, int(view_width * 0.015))
        inner_border_width = max(1, int(view_width * 0.015))
        view_width = view_width - (outer_border_width) - (inner_border_width)
        return view_width