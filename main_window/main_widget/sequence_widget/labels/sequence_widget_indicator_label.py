from typing import TYPE_CHECKING

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceWidgetIndicatorLabel(BaseIndicatorLabel):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget

    def resizeEvent(self, event) -> None:
        self.setFixedHeight(self.sequence_widget.height() // 20)
        font = self.font()
        font.setPointSize(self.sequence_widget.width() // 75)
        self.setFont(font)
