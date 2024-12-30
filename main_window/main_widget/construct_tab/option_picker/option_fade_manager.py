from PyQt6.QtCore import (
    QObject,
    QPropertyAnimation,
    QEasingCurve,
    pyqtSlot,
    QParallelAnimationGroup,
)
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from .scroll_area.section_manager.option_picker_section_widget import (
        OptionPickerSectionWidget,
    )
    from .option_picker import OptionPicker

logger = logging.getLogger(__name__)


class OptionFadeManager(QObject):
    """Manages fade-out and sequential fade-in animations for multiple widgets."""

    def __init__(self, option_picker: "OptionPicker"):
        super().__init__(option_picker)
        self.option_picker = option_picker
        self.json_manager = self.option_picker.json_manager
        self.reversal_filter = self.option_picker.reversal_filter
        self.option_getter = self.option_picker.option_getter
        self.scroll_area = self.option_picker.scroll_area

        self.fade_out_group = None
        self.fade_in_group = None

    def fade_option_picker(self):
        self.fade_out_group = QParallelAnimationGroup(self)

        for section in self.option_picker.get_sections():
            animation = self.fade_out(section)
            self.fade_out_group.addAnimation(animation)

        self.fade_out_group.finished.connect(self.on_fade_out_finished)
        self.fade_out_group.start()

    def fade_out(
        self, section: "OptionPickerSectionWidget", duration: int = 200
    ) -> QPropertyAnimation:
        animation = QPropertyAnimation(section.pictograph_frame.opacity_effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        return animation

    def fade_in(
        self, section: "OptionPickerSectionWidget", duration: int = 200
    ) -> QPropertyAnimation:
        animation = QPropertyAnimation(section.pictograph_frame.opacity_effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        return animation

    @pyqtSlot()
    def on_fade_out_finished(self):
        """Called after all fade-out animations finish. Update pictographs and start fade-in."""
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        selected_filter = self.reversal_filter.reversal_combobox.currentData()
        next_options = self.option_getter.get_next_options(
            sequence, selected_filter
        )
        self.scroll_area.display_manager.clear_all_section_layouts()
        self.scroll_area.add_and_display_relevant_pictographs(next_options)
        sections = self.option_picker.get_sections()
        self.fade_in_group = QParallelAnimationGroup(self)

        for section in sections:
            animation = self.fade_in(section)
            self.fade_in_group.addAnimation(animation)

        self.fade_in_group.start()
        self.fade_in_group.finished.connect(self._on_fade_in_finished)

    @pyqtSlot()
    def _on_fade_in_finished(self):
        for section in self.option_picker.get_sections():
            section.setGraphicsEffect(None)
