from PyQt6.QtCore import QPropertyAnimation, QRect, QPoint, QEasingCurve, QObject
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QSpacerItem,
    QSizePolicy,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class GraphEditorToggler(QObject):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.graph_editor = sequence_widget.graph_editor
        self.toggle_tab = sequence_widget.toggle_tab
        self.graph_editor_placeholder = (
            sequence_widget.layout_manager.graph_editor_placeholder
        )
        self.button_panel_bottom_placeholder = (
            sequence_widget.button_panel.bottom_placeholder
        )  # Bottom spacer in button panel

    def toggle(self):
        if self.graph_editor.isVisible():
            self.animate_graph_editor(show=False)
        else:
            self.sequence_widget.layout_manager.add_graph_editor_placeholder()
            self.graph_editor.show()
            self.animate_graph_editor(show=True)

    def animate_graph_editor(self, show):
        parent_height = self.sequence_widget.height()
        parent_width = self.sequence_widget.width()
        desired_height = self.sequence_widget.graph_editor.get_graph_editor_height()

        # Define start and end values for animation
        if show:
            editor_start_rect = QRect(0, parent_height, parent_width, 0)
            editor_end_rect = QRect(
                0, parent_height - desired_height, parent_width, desired_height
            )
            toggle_start_pos = QPoint(0, parent_height - self.toggle_tab.height())
            toggle_end_pos = QPoint(
                0, parent_height - desired_height - self.toggle_tab.height()
            )
            placeholder_start_height = 0
            placeholder_end_height = desired_height
        else:
            editor_start_rect = QRect(
                0, parent_height - desired_height, parent_width, desired_height
            )
            editor_end_rect = QRect(0, parent_height, parent_width, 0)
            toggle_start_pos = QPoint(
                0, parent_height - desired_height - self.toggle_tab.height()
            )
            toggle_end_pos = QPoint(0, parent_height - self.toggle_tab.height())
            placeholder_start_height = desired_height
            placeholder_end_height = 0

        # Animate GraphEditor geometry
        self.graph_editor_animation = QPropertyAnimation(self.graph_editor, b"geometry")
        self.graph_editor_animation.setStartValue(editor_start_rect)
        self.graph_editor_animation.setEndValue(editor_end_rect)
        self.graph_editor_animation.setDuration(300)
        self.graph_editor_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Animate graph editor placeholder height
        self.graph_editor_placeholder_animation = QPropertyAnimation(
            self.graph_editor_placeholder, b"minimumHeight"
        )
        self.graph_editor_placeholder_animation.setStartValue(placeholder_start_height)
        self.graph_editor_placeholder_animation.setEndValue(placeholder_end_height)
        self.graph_editor_placeholder_animation.setDuration(300)
        self.graph_editor_placeholder_animation.setEasingCurve(
            QEasingCurve.Type.OutQuad
        )

        # Remove placeholder on collapse
        if not show:
            self.graph_editor_animation.finished.connect(
                lambda: self.sequence_widget.layout_manager.remove_graph_editor_placeholder()
            )
            self.graph_editor_animation.finished.connect(self.graph_editor.hide)

        # Animate toggle tab position
        self.toggle_tab_animation = QPropertyAnimation(self.toggle_tab, b"pos")
        self.toggle_tab_animation.setStartValue(toggle_start_pos)
        self.toggle_tab_animation.setEndValue(toggle_end_pos)
        self.toggle_tab_animation.setDuration(300)
        self.toggle_tab_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Start all animations simultaneously
        self.graph_editor_animation.start()
        self.graph_editor_placeholder_animation.start()
        self.toggle_tab_animation.start()
        # self.sequence_widget.button_panel.resize_button_panel()
