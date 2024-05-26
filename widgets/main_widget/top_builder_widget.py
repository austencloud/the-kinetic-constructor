from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QPainter


from widgets.sequence_builder.sequence_builder import SequenceBuilder
from widgets.sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class TopBuilderWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget

        self.background_manager = (
            self.main_widget.main_window.settings_manager.setup_background_manager(self)
        )

        self.sequence_builder = SequenceBuilder(self)
        self.sequence_widget = SequenceWidget(self)
        self.initialized = False
        self._setup_layout()
        self.connect_signals()

    def connect_signals(self):
        self.main_widget.main_window.settings_manager.background_changed.connect(
            self.update_background_manager
        )

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.sequence_widget, 1)
        self.layout.addWidget(self.sequence_builder, 1)

    def update_background_manager(self, bg_type: str):
        self.background_manager = (
            self.main_widget.main_window.settings_manager.setup_background_manager(self)
        )
        self.background_manager.update_required.connect(self.update)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)
