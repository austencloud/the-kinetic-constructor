from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QPainter
from .sequence_builder.sequence_builder import SequenceBuilder
from .sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class TopBuilderWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget

        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )

        self.sequence_builder = SequenceBuilder(self.main_widget)
        self.sequence_widget = self.main_widget.sequence_widget
        self.initialized = False
        self._setup_layout()
        self.background_manager = None

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.sequence_widget, 1)
        self.layout.addWidget(self.sequence_builder, 1)

    def update_background_manager(self, bg_type: str):
        if self.background_manager:
            self.background_manager.stop_animation()
        self.background_manager = self.global_settings.setup_background_manager(self)
        self.background_manager.update_required.connect(self.update)
        self.background_manager.start_animation()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)

    def showEvent(self, event):
        super().showEvent(event)
        if self.background_manager is None:
            self.background_manager = self.global_settings.setup_background_manager(
                self
            )
        self.background_manager.start_animation()

    def hideEvent(self, event):
        super().hideEvent(event)
        if self.background_manager:
            self.background_manager.stop_animation()

    def resize_top_builder_widget(self):
        self.sequence_widget.resize_sequence_widget()
        self.sequence_builder.resize_sequence_builder()
        self.sequence_widget.beat_frame.selection_overlay.update_overlay_position()
