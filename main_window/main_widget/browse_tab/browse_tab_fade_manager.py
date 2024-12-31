from PyQt6.QtCore import (
    QObject,
    QPropertyAnimation,
    QEasingCurve,
    pyqtSlot,
    QParallelAnimationGroup,
)
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget, QApplication

from typing import TYPE_CHECKING
import logging

from main_window.main_widget.browse_tab.sequence_picker.filter_selector.filter_section_base import (
    FilterSectionBase,
)


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab
    from main_window.main_widget.construct_tab.construct_tab import ConstructTab


logger = logging.getLogger(__name__)


class BrowseTabFadeManager(QObject):
    """Manages fade-out and sequential fade-in animations for multiple widgets."""

    def __init__(self, browse_tab: "BrowseTab") -> None:
        super().__init__(browse_tab)
        self.browse_tab = browse_tab

        self.fade_out_group = None
        self.fade_in_group = None

    def fade_and_update_browse_tab(self):
        self.fade_out_group = QParallelAnimationGroup(self)

        animation = self.fade_out_filter_stack()
        self.fade_out_group.addAnimation(animation)

        self.fade_out_group.finished.connect(self.on_fade_out_finished)
        self.fade_out_group.start()

    def fade_out_filter_stack(self) -> QPropertyAnimation:
        opacity_effect = QGraphicsOpacityEffect()
        self.browse_tab.sequence_picker.filter_stack.setGraphicsEffect(opacity_effect)
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(200)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        return animation

    def fade_in_sequence_picker(
        self,
    ) -> QPropertyAnimation:
        opacity_effect = QGraphicsOpacityEffect()
        self.browse_tab.sequence_picker.setGraphicsEffect(opacity_effect)
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(200)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        return animation

    @pyqtSlot()
    def on_fade_out_finished(self):
        """Called after all fade-out animations finish. Update pictographs and start fade-in."""
        self.browse_tab.filter_manager.sort_and_display_thumbnail_boxes_by_current_filter(
            self.browse_tab.filter_manager.current_filter
        )
        QApplication.processEvents()
        self.browse_tab.main_widget.left_stack.setCurrentIndex(
            self.browse_tab.main_widget.left_sequence_picker_index
        )
        self.fade_in_group = QParallelAnimationGroup(self)

        animation = self.fade_in_sequence_picker()
        self.fade_in_group.addAnimation(animation)

        self.fade_in_group.start()
        self.fade_in_group.finished.connect(self._on_fade_in_finished)

    @pyqtSlot()
    def _on_fade_in_finished(self):
        self.clear_graphics_effects()

    def clear_graphics_effects(self) -> None:
        """Recursively clears GraphicsEffect from the given widget and its children."""
        self.browse_tab.sequence_picker.filter_stack.setGraphicsEffect(None)
        self.browse_tab.sequence_picker.setGraphicsEffect(None)
