from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt6.QtCore import QSequentialAnimationGroup, QPointF, QPropertyAnimation, Qt

from widgets.animated_pictograph.animated_pictograph_initializer import (
    AnimatedPictographInitializer,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.animator import Animator
    from widgets.sequence_widget.sequence_modifier import SequenceModifier


class AnimatedPictograph(QGraphicsScene):
    def __init__(self, animator: "Animator") -> None:
        super().__init__(animator)
        self.main_widget = animator.main_widget
        self.animation_group = QSequentialAnimationGroup()
        self.view = None
        self.initializer = AnimatedPictographInitializer(self)
        self.initializer.init_all_components()

    def add_prop(self, prop):
        self.addItem(prop)

    def animate_prop(self, prop, startPos, endPos, duration=1000):
        animation = QPropertyAnimation(prop, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(startPos)
        animation.setEndValue(endPos)
        self.animation_group.addAnimation(animation)

    def start_animations(self):
        self.animation_group.start()

    def setup_animation_for_sequence(self, current_sequence):
        beat = current_sequence[0]
        for beat in current_sequence:
            prop = self.create_prop_from_beat(beat)
            startPos = QPointF(beat["startPosX"], beat["startPosY"])
            endPos = QPointF(beat["endPosX"], beat["endPosY"])
            self.add_prop(prop)
            self.animate_prop(prop, startPos, endPos)

        self.start_animations()


class AnimatedPictographView(QGraphicsView):
    def __init__(
        self,
        animated_pictograph: AnimatedPictograph,
        animator: "Animator",
    ) -> None:
        super().__init__(animated_pictograph, animator)
        self.setScene(animated_pictograph)
        self.animated_pictograph = animated_pictograph
        animated_pictograph.view = self
        self.animator = animator

    def resize_animated_pictograph_view(self):
        self.setMinimumHeight(self.animator.height())
        self.setMinimumWidth(self.animator.height())
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def set_to_blank_grid(self):
        self.setScene(self.animated_pictograph)
