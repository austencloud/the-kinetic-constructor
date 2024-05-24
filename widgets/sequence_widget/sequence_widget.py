from typing import TYPE_CHECKING
from PyQt6.QtGui import QShowEvent
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QSpinBox,
    QScrollArea,
    QComboBox,
)

from widgets.graph_editor.graph_editor import GraphEditor
from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame
from widgets.sequence_widget.SW_beat_frame.SW_options_panel import SW_OptionsPanel
from widgets.sequence_widget.my_sequence_label import MySequenceLabel
from widgets.sequence_widget.sequence_modifier import SequenceModifier
from ..indicator_label import IndicatorLabel
from .SW_pictograph_factory import (
    SW_PictographFactory,
)
from .SW_beat_frame.beat import Beat

from .SW_button_frame import SW_ButtonFrame
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget.top_builder_widget import TopBuilderWidget


class SequenceWidget(QWidget):
    def __init__(self, top_builder_widget: "TopBuilderWidget") -> None:
        super().__init__()
        self.top_builder_widget = top_builder_widget
        self.main_widget = top_builder_widget.main_widget

        self._setup_components()
        self._setup_cache()
        self._setup_beat_frame_layout()
        self._setup_indicator_label_layout()
        self._setup_layout()

    def _setup_cache(self):
        self.SW_pictograph_cache: dict[str, Beat] = {}

    def _setup_components(self):
        self.indicator_label = IndicatorLabel(self)
        self.beat_frame = SW_BeatFrame(self)
        self.button_frame = SW_ButtonFrame(self)
        self.graph_editor = GraphEditor(self)
        self.pictograph_factory = SW_PictographFactory(self)
        self.my_sequence_label = MySequenceLabel(self)

        # self._setup_options_button()

        self.beat_combo_box = QComboBox(self)
        self.beat_combo_box.addItems([str(i) for i in range(1, 65)])
        self.beat_combo_box.setCurrentIndex(15)  # Default index for 16 beats
        self.beat_combo_box.currentIndexChanged.connect(
            lambda index: self.beat_frame.layout_manager.configure_beat_frame(index + 1)
        )

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.beat_frame)
        self.scroll_area.setObjectName("sequence_scroll_area")
        self.scroll_area.setStyleSheet("QScrollArea{background: transparent;}")
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

    def show_options_panel(self):
        self.options_panel = SW_OptionsPanel(self)
        self.options_panel.exec()  # Use exec() to show the dialog modally

    def apply_options(self, grow_sequence, rows, cols, num_beats, save_layout):
        self.grow_sequence = grow_sequence
        if grow_sequence:
            # Logic for growing sequence automatically
            pass  # Implement your logic for growing the sequence
        else:
            self.beat_frame.layout_manager.rearrange_beats(num_beats, cols, rows)
        if save_layout:
            self.save_layout_as_default(rows, cols)

    def save_layout_as_default(self, rows, cols):
        # Implement logic to save layout as default
        pass

    def _setup_beat_frame_layout(self):
        self.beat_frame_layout = QHBoxLayout()
        self.beat_frame_layout.addWidget(self.scroll_area)
        self.beat_frame_layout.addWidget(self.button_frame)
        self.beat_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.beat_frame_layout.setSpacing(0)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.my_sequence_label, stretch=1)
        self.layout.addWidget(self.beat_combo_box, stretch=1)
        self.layout.addLayout(self.beat_frame_layout, stretch=35)
        self.layout.addWidget(self.indicator_label, stretch=1)
        self.layout.addWidget(self.graph_editor, stretch=6)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        self.layout.update()
        super().resizeEvent(event)

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        QTimer.singleShot(0, self.post_show_initialization)

    def post_show_initialization(self):
        self.resize_sequence_widget()
        self.beat_frame.layout_manager.configure_beat_frame(
            self.beat_combo_box.currentIndex() + 1
        )

    def _setup_indicator_label_layout(self):
        self.indicator_label_layout = QHBoxLayout()
        self.indicator_label_layout.addStretch(1)
        self.indicator_label_layout.addWidget(self.indicator_label)
        self.indicator_label_layout.addStretch(1)

    def populate_sequence(self, pictograph_dict: dict) -> None:
        pictograph = Beat(self.beat_frame)
        pictograph.updater.update_pictograph(pictograph_dict)
        self.beat_frame.add_beat_to_sequence(pictograph)
        pictograph_key = (
            pictograph.main_widget.pictograph_key_generator.generate_pictograph_key(
                pictograph_dict
            )
        )
        self.SW_pictograph_cache[pictograph_key] = pictograph

    def resize_sequence_widget(self) -> None:
        self.my_sequence_label.resize_my_sequence_label()
        self.beat_frame.resize_beat_frame()
        self.graph_editor.resize_graph_editor()
        self.button_frame.resize_button_frame()
