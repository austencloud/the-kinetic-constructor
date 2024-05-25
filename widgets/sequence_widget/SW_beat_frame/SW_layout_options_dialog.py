from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QCheckBox,
    QLabel,
    QGridLayout,
    QWidget,
    QComboBox,
)
from PyQt6.QtCore import Qt

from widgets.sequence_widget.SW_beat_frame.beat import BeatView
from widgets.sequence_widget.SW_beat_frame.layout_options_panel import (
    LayoutOptionsPanel,
)
from widgets.sequence_widget.SW_beat_frame.layout_options_preview import (
    LayoutOptionsPreview,
)
from widgets.sequence_widget.SW_beat_frame.layout_warning_dialog import (
    LayoutWarningDialog,
)
from widgets.sequence_widget.SW_beat_frame.start_pos_beat import StartPositionBeatView

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SW_LayoutOptionsDialog(QDialog):
    def __init__(
        self, sequence_widget: "SequenceWidget", initial_state: Optional[dict] = None
    ):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.settings_manager = (
            self.sequence_widget.main_widget.main_window.settings_manager
        )
        self.setWindowTitle("Layout Options")
        self.layout_options = {
            1: [(1, 1)],
            2: [(1, 2)],
            3: [(1, 3), (2, 2)],
            4: [(2, 2), (1, 4)],
            6: [(3, 2), (2, 3)],
            8: [(4, 2), (2, 4)],
            7: [(4, 2), (2, 4)],
            9: [(3, 3), (2, 5), (5, 2)],
            10: [(5, 2), (2, 5)],
            11: [(4, 3), (3, 4)],
            12: [(4, 3), (3, 4)],
            13: [(5, 3), (3, 5)],
            14: [(4, 4), (2, 7), (7, 2)],
            15: [(5, 3), (3, 5)],
            16: [(4, 4), (2, 8), (8, 2)],
        }

        self._set_size()

        self.panel = LayoutOptionsPanel(self)
        self.preview = LayoutOptionsPreview(self)

        self._setup_main_layout()
        self._setup_layout_options()

        if initial_state:
            self.panel.initialize_from_state(initial_state)
        else:
            self.panel.load_settings()

    def _set_size(self):
        main_widget_size = self.sequence_widget.main_widget.size()
        self.setFixedSize(
            int(main_widget_size.width() // 3), int(main_widget_size.height() // 2)
        )

    def _setup_main_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.preview, 3)
        self.main_layout.addWidget(self.panel, 1)

    def _setup_layout_options(self):
        self.panel.layout_combo_box.clear()
        num_beats = int(self.panel.beats_combo_box.currentText())
        layouts = self.layout_options.get(num_beats, [])
        for layout in layouts:
            self.panel.layout_combo_box.addItem(f"{layout[0]} x {layout[1]}")
        if layouts:
            self.panel.layout_combo_box.setCurrentIndex(0)

    def update_preview(self):
        self.preview.update_preview()

    def apply_settings(self):
        grow_sequence = self.panel.sequence_growth_checkbox.isChecked()
        num_filled_beats = (
            self.sequence_widget.beat_frame.find_next_available_beat() - 1 or 0
        )
        if grow_sequence:
            self.settings_manager.set_grow_sequence(True)
            self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
                num_filled_beats + 1
            )
        else:
            self.settings_manager.set_grow_sequence(False)
            num_beats = int(self.panel.beats_combo_box.currentText())
            selected_layout = self.panel.layout_combo_box.currentText()
            rows, cols = map(int, selected_layout.split(" x "))
            if num_beats < num_filled_beats:
                if self.open_warning_dialog():
                    self.sequence_widget.apply_layout_options(rows, cols, num_beats)
                    # clear the remaining beats
                    for i in range(num_beats, num_filled_beats):
                        self.sequence_widget.beat_frame.beats[i].setScene(
                            self.sequence_widget.beat_frame.beats[i].blank_beat
                        )
                    # Update the selection overlay
                    self.sequence_widget.beat_frame.selection_manager.select_beat(
                        self.sequence_widget.beat_frame.beats[num_beats - 1]
                    )
            else:
                self.sequence_widget.apply_layout_options(rows, cols, num_beats)
        self.accept()

    def open_warning_dialog(self):
        dialog = LayoutWarningDialog(self)
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted
