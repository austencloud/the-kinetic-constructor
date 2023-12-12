from typing import TYPE_CHECKING

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy, QGraphicsView

from widgets.graph_editor.object_panel.arrowbox.arrowbox import ArrowBox
from widgets.graph_editor.object_panel.objectbox_view import ObjectBoxView
from widgets.graph_editor.pictograph.pictograph import Pictograph
from widgets.graph_editor.object_panel.propbox.propbox import PropBox
from widgets.graph_editor.attr_panel.attr_panel import AttrPanel
from widgets.graph_editor.pictograph.pictograph_view import PictographView

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class GraphEditor(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self._initialize_main_widget_attributes(main_widget)
        self._setup_frame_style()
        self._setup_main_layout()
        self._create_child_widgets(main_widget)
        self._add_widgets_to_layouts()
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
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _create_child_widgets(self, main_widget: "MainWidget") -> None:
        self.pictograph = Pictograph(main_widget, self)
        self.arrowbox = ArrowBox(main_widget, self)
        self.propbox = PropBox(main_widget, self)
        self.attr_panel = AttrPanel(self)

    def _add_widgets_to_layouts(self) -> None:
        self.objectbox_layout = QVBoxLayout()
        self.pictograph_layout = QVBoxLayout()
        self.attr_panel_layout = QVBoxLayout()

        self.objectbox_layout.addWidget(self.arrowbox.view)
        self.objectbox_layout.addWidget(self.propbox.view)
        self.pictograph_layout.addWidget(self.pictograph.view)
        self.attr_panel_layout.addWidget(self.attr_panel)

        self.layout.addLayout(self.objectbox_layout)
        self.layout.addLayout(self.pictograph_layout)
        self.layout.addLayout(self.attr_panel_layout)

    def _apply_layout(self) -> None:
        self.setLayout(self.layout)

    def _setup_size_policy(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _fit_view_in_aspect_ratio(self, view: QGraphicsView) -> None:
        """
        Fits the view of a widget within its scene's rectangle while maintaining the aspect ratio.
        This method is particularly useful for graphical widgets like Pictograph, ArrowBox, and PropBox.
        """
        view.fitInView(view.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def _set_objectbox_view_size(
        self, view: ObjectBoxView, reference_view: PictographView
    ) -> None:
        """
        Sets the minimum size for a widget based on the dimensions of a reference widget.
        """
        view.setMinimumSize(int(reference_view.height() / 2), reference_view.height())

    def resizeEvent(self, event) -> None:
        """
        Handles the resizing of GraphEditor and its child widgets.
        This method is automatically called whenever the GraphEditor widget is resized.
        """
        super().resizeEvent(event)
        self._adjust_child_widgets_size()
        self._adjust_graph_editor_size()
        

    def _adjust_graph_editor_size(self) -> None:
        """
        Adjusts the maximum height of the GraphEditor relative to its parent widget's height.
        This ensures that the GraphEditor does not become disproportionately large or small.
        """
        self.setMaximumHeight(int(self.main_widget.height() / 2))

    def _adjust_child_widgets_size(self) -> None:
        """
        Adjusts the size of child widgets to maintain a consistent layout and aspect ratio
        during the resize event. This includes setting minimum widths and fitting views
        within their respective scenes while maintaining aspect ratios.
        """
        # Adjust the size and view of the Pictograph widget
        self._fit_view_in_aspect_ratio(self.pictograph.view)
        self.pictograph.view.setMaximumHeight(self.height())

        # Adjust the size and view of the ArrowBox widget
        self._set_objectbox_view_size(self.arrowbox.view, self.pictograph.view)
        self._fit_view_in_aspect_ratio(self.arrowbox.view)

        # Adjust the size and view of the PropBox widget
        self._set_objectbox_view_size(self.propbox.view, self.pictograph.view)
        self._fit_view_in_aspect_ratio(self.propbox.view)
