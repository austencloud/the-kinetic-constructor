from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect
from .graph_editor_layout_manager import GraphEditorLayoutManager
from .graph_editor_state_manager import GraphEditorStateManager
from .graph_editor_toggle_tab import GraphEditorToggleTab
from .graph_editor_animator import GraphEditorAnimator
from .adjustment_panel.beat_adjustment_panel import BeatAdjustmentPanel
from .pictograph_container.GE_pictograph_container import GraphEditorPictographContainer

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


# graph_editor.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class GraphEditor(QFrame):
    pictograph_layout: QVBoxLayout
    adjustment_panel_layout: QVBoxLayout

    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        # Set size policies
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setMinimumHeight(0)  # Allow to shrink to zero height
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._setup_components()
        self.layout_manager.setup_layout()
        self.hide()

    def _setup_components(self) -> None:
        self.pictograph_container = GraphEditorPictographContainer(self)
        self.adjustment_panel = BeatAdjustmentPanel(self)
        self.toggle_tab = GraphEditorToggleTab(self)
        self.layout_manager = GraphEditorLayoutManager(self)
        self.state = GraphEditorStateManager(self)
        # self.animator = GraphEditorAnimator(self)
        self.toggle_tab.toggled.connect(self.toggle_graph_editor)

        # Set size policies for child widgets
        self.pictograph_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.pictograph_container.setMinimumHeight(0)

        self.adjustment_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.adjustment_panel.setMinimumHeight(0)

    def toggle_graph_editor(self):
        if self.isVisible():
            self.animate_graph_editor(show=False)
        else:
            self.show()
            self.animate_graph_editor(show=True)

    def animate_graph_editor(self, show):
        parent_height = self.sequence_widget.height()
        parent_width = self.sequence_widget.width()
        desired_height = int(parent_height // 3.5)  # Or whatever height you desire

        if show:
            start_rect = QRect(0, parent_height, parent_width, 0)
            end_rect = QRect(
                0, parent_height - desired_height, parent_width, desired_height
            )
            self.sequence_widget.scroll_area.setFixedHeight(
                self.sequence_widget.height()
                - desired_height
                - self.sequence_widget.current_word_label.height()
                - self.sequence_widget.difficulty_label.height()
                - self.toggle_tab.height()
                - 150
            )
            # set the stretch of the beat frame layout in the layout manager of the sequence widget to be 8
            self.sequence_widget.layout_manager.main_layout.setStretch(1, 2)
        else:
            start_rect = QRect(
                0, parent_height - desired_height, parent_width, desired_height
            )
            end_rect = QRect(0, parent_height, parent_width, 0)
            self.sequence_widget.scroll_area.setFixedHeight(
                self.sequence_widget.height()
                - self.sequence_widget.current_word_label.height()
                - self.sequence_widget.difficulty_label.height()
                - self.toggle_tab.height()
                - 150
            )

        self.setGeometry(start_rect)

        animation = QPropertyAnimation(self, b"geometry")
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        if not show:
            animation.finished.connect(self.hide)
        animation.start()
        self.current_animation = animation  # Keep a reference

    def resize_graph_editor(self) -> None:
        # Remove the move() call; position will be managed in animate_graph_editor()
        self.setFixedSize(
            self.sequence_widget.width(), int(self.sequence_widget.height() // 3.5)
        )
        self.pictograph_container.resize_GE_pictograph_container()
        self.adjustment_panel.update_adjustment_panel()
        self.adjustment_panel.placeholder_widget.resize_adjustment_panel_placeholder_text()
        self.adjustment_panel.resize_beat_adjustment_panel()
        self.raise_()  # Ensure it appears above other widgets
        self.toggle_tab.raise_()

    def resizeEvent(self, event):
        self.resize_graph_editor()
        super().resizeEvent(event)
