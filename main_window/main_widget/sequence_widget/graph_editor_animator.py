from typing import TYPE_CHECKING
from PyQt6.QtCore import (
    QObject,
    QPropertyAnimation,
    QEasingCurve,
    QSequentialAnimationGroup,
    QPoint,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget
    from main_window.main_widget.sequence_widget.graph_editor.graph_editor import (
        GraphEditor,
    )


class GraphEditorAnimator(QObject):
    def __init__(self, graph_editor: "GraphEditor"):
        super().__init__()
        self.graph_editor = graph_editor
        self.sequence_widget = graph_editor.sequence_widget
        self.toggle_tab = self.graph_editor.toggle_tab
        self.is_animating = False

        # Initialize animations
        self.graph_editor_animation = QPropertyAnimation(
            self.graph_editor, b"maximumHeight"
        )
        self.graph_editor_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.graph_editor_animation.setDuration(300)

        self.toggle_tab_animation = QPropertyAnimation(self.toggle_tab, b"pos")
        self.toggle_tab_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.toggle_tab_animation.setDuration(300)

        # Group both animations
        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.graph_editor_animation)
        self.animation_group.addAnimation(self.toggle_tab_animation)
        self.animation_group.finished.connect(self.animation_finished)

    def animate_toggle(self):
        self.is_animating = True
        editor_height = self.sequence_widget.main_widget.height() // 4

        if self.graph_editor.is_graph_editor_visible:
            # Collapse to zero height
            self.graph_editor_animation.setStartValue(self.graph_editor.height())
            self.graph_editor_animation.setEndValue(0)

            # Move toggle to bottom
            toggle_bottom_position = QPoint(
                self.toggle_tab.pos().x(),
                self.sequence_widget.height() - self.toggle_tab.height(),
            )
            self.toggle_tab_animation.setStartValue(self.toggle_tab.pos())
            self.toggle_tab_animation.setEndValue(toggle_bottom_position)
            self.graph_editor.is_graph_editor_visible = False
        else:
            # Expand graph editor to full height
            self.graph_editor_animation.setStartValue(0)
            self.graph_editor_animation.setEndValue(editor_height)

            # Reset toggle tab to above GraphEditor
            toggle_top_position = self.graph_editor.pos() - QPoint(
                0, self.toggle_tab.height()
            )
            self.toggle_tab_animation.setStartValue(self.toggle_tab.pos())
            self.toggle_tab_animation.setEndValue(toggle_top_position)
            self.graph_editor.is_graph_editor_visible = True

        self.animation_group.start()

    def animation_finished(self):
        self.is_animating = False
        self.graph_editor.save_graph_editor_state()
