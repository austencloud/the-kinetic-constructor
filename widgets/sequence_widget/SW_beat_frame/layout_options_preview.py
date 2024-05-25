from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGridLayout, QWidget
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_layout_options_dialog import (
        SW_LayoutOptionsDialog,
    )
from widgets.sequence_widget.SW_beat_frame.beat import BeatView
from widgets.sequence_widget.SW_beat_frame.start_pos_beat import StartPositionBeatView


class LayoutOptionsPreview(QWidget):
    def __init__(self, dialog: "SW_LayoutOptionsDialog"):
        super().__init__(dialog)
        self.dialog = dialog
        self.sequence_widget = dialog.sequence_widget

        self._setup_layout()

    def _setup_layout(self):
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_preview(self):
        layout = self.layout
        for i in reversed(range(layout.count())):
            widget_to_remove = layout.itemAt(i).widget()
            layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        if not self.dialog.panel.sequence_growth_checkbox.isChecked():
            num_beats = int(self.dialog.panel.beats_combo_box.currentText())
            selected_layout = self.dialog.panel.layout_combo_box.currentText()
            if selected_layout:
                rows, cols = map(int, selected_layout.split(" x "))

                cols_with_start_pos = cols + 1
                rows_with_start_pos = rows + 1
                preview_size = min(
                    (self.dialog.width() // 2) // cols_with_start_pos,
                    self.dialog.height() // rows_with_start_pos,
                )
                beat_size = preview_size

                if layout.count() == 0:
                    start_pos_view = StartPositionBeatView(
                        self.sequence_widget.beat_frame
                    )
                    start_pos_view.setFixedSize(beat_size, beat_size)
                    layout.addWidget(start_pos_view, 0, 0)

                    beat_index = 0
                    for row in range(rows):
                        for col in range(1, cols + 1):
                            if beat_index < num_beats:
                                beat_view = BeatView(
                                    self.sequence_widget.beat_frame, beat_index + 1
                                )
                                beat_view.setFixedSize(beat_size, beat_size)
                                beat_view.resize_beat_view()
                                layout.addWidget(beat_view, row, col)
                                beat_index += 1
