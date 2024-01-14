from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy
from widgets.graph_editor_tab.graph_editor_attr_panel import GraphEditorAttrPanel
from widgets.graph_editor_tab.graph_editor_pictograph import GraphEditorPictograph

from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox import (
    ArrowBox,
)
from widgets.graph_editor_tab.graph_editor_pictograph_widget import (
    GraphEditorPictographWidget,
)
from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox import PropBox

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor_tab import GraphEditorTab


class GraphEditorFrame(QFrame):
    def __init__(
        self, main_widget: "MainWidget", graph_editor_tab: "GraphEditorTab"
    ) -> None:
        super().__init__()
        self._setup_main_widget_attributes(main_widget)
        # self._setup_frame_style()
        self._create_children(main_widget)
        self._setup_main_layout()
        self._apply_layout()
        self._setup_size_policy()

    def _setup_main_widget_attributes(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.main_window = main_widget.main_window

    def _setup_frame_style(self) -> None:
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

    def _setup_main_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.objectbox_layout = QVBoxLayout()
        self.pictograph_layout = QVBoxLayout()
        self.attr_panel_layout = QVBoxLayout()

        self.objectbox_layout.addWidget(self.arrowbox.view)
        self.objectbox_layout.addWidget(self.propbox.view)
        self.pictograph_layout.addWidget(self.pictograph_widget)
        self.attr_panel_layout.addWidget(self.attr_panel)

        self.layout.addStretch(1)
        self.layout.addLayout(self.objectbox_layout)
        self.layout.addLayout(self.pictograph_layout)
        self.layout.addLayout(self.attr_panel_layout)
        self.layout.addStretch(1)

        self.objectbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setAlignment(self.main_widget, Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.layout)

    def _create_children(self, main_widget: "MainWidget") -> None:
        self.main_pictograph = GraphEditorPictograph(main_widget, self)
        self.arrowbox = ArrowBox(main_widget, self)
        self.propbox = PropBox(main_widget, self)
        self.attr_panel = GraphEditorAttrPanel(self)

        self.pictograph_widget = GraphEditorPictographWidget(
            self, self.main_pictograph.view
        )

    def _apply_layout(self) -> None:
        self.setLayout(self.layout)

    def _setup_size_policy(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
