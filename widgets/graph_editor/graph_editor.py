from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy
from widgets.graph_editor.main_pictograph import MainPictograph

from widgets.graph_editor.object_panel.arrowbox.arrowbox import ArrowBox
from widgets.graph_editor.main_pictograph_widget import MainPictographWidget
from widgets.graph_editor.object_panel.propbox.propbox import PropBox
from widgets.graph_editor.attr_panel.attr_panel import AttrPanel

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graph_editor_widget import GraphEditorWidget


class GraphEditor(QFrame):
    def __init__(
        self, main_widget: "MainWidget", graph_editor_widget: "GraphEditorWidget"
    ) -> None:
        super().__init__()
        self._initialize_main_widget_attributes(main_widget)
        self._setup_frame_style()
        self._create_children(main_widget)
        self._setup_main_layout()
        self._apply_layout()
        self._setup_size_policy()

    def _initialize_main_widget_attributes(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.json_handler = main_widget.json_handler

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

        self.setLayout(self.layout)

    def preferred_height(self) -> int:
        return self.pictograph_widget.calculate_preferred_height()

    def _create_children(self, main_widget: "MainWidget") -> None:
        self.main_pictograph = MainPictograph(main_widget, self)
        self.arrowbox = ArrowBox(main_widget, self)
        self.propbox = PropBox(main_widget, self)
        self.attr_panel = AttrPanel(self)

        self.pictograph_widget = MainPictographWidget(
            self, self.main_pictograph.view, 75 / 90
        )

    def _apply_layout(self) -> None:
        self.setLayout(self.layout)

    def _setup_size_policy(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
