from typing import TYPE_CHECKING
from PyQt6.QtGui import QShowEvent

from widgets.graph_editor_widget.graph_editor import GraphEditor

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy


class GraphEditorWidget(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.main_layout = QHBoxLayout(self)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.graph_editor = GraphEditor(self.main_widget, self)

        self.main_layout.addWidget(self.graph_editor)

    def showEvent(self, event: QShowEvent) -> None:
        content_width = int(
            self.graph_editor.arrowbox.view.width()
            + self.graph_editor.pictograph_widget.main_pictograph_view.width()
            + self.graph_editor.attr_panel.width()
        )

        # self.main_widget.right_frame.setMinimumWidth(content_width)
        self.graph_editor.setMaximumHeight(
            self.graph_editor.pictograph_widget.main_pictograph_view.height()
        )
        self.main_widget.right_frame.setMaximumWidth(content_width)
        self.graph_editor.setMaximumWidth(content_width)
        self.setMaximumWidth(content_width)
