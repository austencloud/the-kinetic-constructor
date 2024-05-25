from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QPainter


from background_managers.background_manager import (
    AttractionParticlesBackgroundManager,
    AuroraBackgroundManager,
    AuroraBorealisBackgroundManager,
    ParticleBackgroundManager,
    RainbowBackgroundManager,
    StarfieldBackgroundManager,
    WaterRipplesBackgroundManager,
)
from widgets.sequence_builder.sequence_builder import SequenceBuilder
from widgets.sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class TopBuilderWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget

        self._setup_background_manager()  # Setup background based on user preferences

        self.sequence_builder = SequenceBuilder(self)
        self.sequence_widget = SequenceWidget(self)
        self.initialized = False
        self._setup_layout()
        self.connect_signals()

    def connect_signals(self):
        self.main_widget.main_window.settings_manager.background_changed.connect(
            self._setup_background_manager
        )

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.sequence_widget, 1)
        self.layout.addWidget(self.sequence_builder, 1)

    def _setup_background_manager(self):
        # Fetch the preferred background type from settings
        bg_type = self.main_widget.main_window.settings_manager.get_setting(
            "background_type", "Rainbow"
        )
        if bg_type == "Rainbow":
            self.background_manager = RainbowBackgroundManager(self)
        elif bg_type == "Starfield":
            self.background_manager = StarfieldBackgroundManager(self)
        elif bg_type == "Particle":
            self.background_manager = ParticleBackgroundManager(self)
        elif bg_type == "Aurora":
            self.background_manager = AuroraBackgroundManager(self)
        elif bg_type == "AuroraBorealis":
            self.background_manager = AuroraBorealisBackgroundManager(self)
        elif bg_type == "AttractionParticles":
            self.background_manager = AttractionParticlesBackgroundManager(self)
        elif bg_type == "WaterRipples":
            self.background_manager = WaterRipplesBackgroundManager(self)
        # Add other conditions for different backgrounds
        self.background_manager.update_required.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)
