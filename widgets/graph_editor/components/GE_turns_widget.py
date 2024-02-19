from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QHBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from widgets.graph_editor.GE_turns_button_manager import GE_TurnsButtonManager
from widgets.graph_editor.GE_turns_widget_display_manager import (
    GE_TurnsWidgetDisplayManager,
)
from widgets.turns_box.turns_box_widgets.turns_widget.managers.sequence_modifier_turns_adjustment_manager import (
    GE_TurnsAdjustmentManager,
)
from widgets.turns_box.turns_box_widgets.turns_widget.managers.turn_direct_set_manager import (
    TurnDirectSetManager,
)
from widgets.turns_box.turns_box_widgets.turns_widget.managers.turns_updater import (
    TurnsUpdater,
)


if TYPE_CHECKING:
    from .GE_turns_box import GE_TurnsBox


class GE_TurnsWidget(QWidget):
    def __init__(self, turns_box: "GE_TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self._setup_layout()
        self._setup_components()
        self._setup_ui()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 4, 0, 0)
        self.layout.setSpacing(0)

    def _setup_components(self):
        self.direct_set_manager = TurnDirectSetManager(self)
        self.display_manager = GE_TurnsWidgetDisplayManager(self)
        self.button_manager = GE_TurnsButtonManager(self)
        self.adjustment_manager = GE_TurnsAdjustmentManager(self)
        self.updater = TurnsUpdater(self)

    def _setup_ui(self) -> None:
        self.button_manager.setup_adjust_turns_buttons()
        self.display_manager.setup_display_components()
        self.direct_set_manager.setup_direct_set_buttons()

    def setup_additional_layouts(self) -> None:
        self.turn_display_and_adjust_btns_hbox_layout = QHBoxLayout()

    ### LAYOUTS ###

    def _setup_layout_frames(self) -> None:
        """Adds the header and buttons to their respective frames."""
        self.turn_display_and_adjust_btns_hbox_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_hbox_layout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = self._create_frame(
            self.turn_display_and_adjust_btns_hbox_layout
        )
        self.button_frame = self._create_frame(self.buttons_hbox_layout)
        self.header_frame.setContentsMargins(0, 0, 0, 0)
        self.button_frame.setContentsMargins(0, 0, 0, 0)

    def setup_additional_layouts(self):
        self.turn_display_and_adjust_btns_hbox_layout = QHBoxLayout()

    def _create_frame(self, layout: QHBoxLayout | QVBoxLayout) -> QFrame:
        """Creates a frame with the given layout."""
        frame = QFrame()
        frame.setLayout(layout)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return frame

    ### WIDGETS ###

    def _create_turnbox_vbox_frame(self) -> None:
        """Creates the turns box and buttons for turn adjustments."""
        turnbox_frame = QFrame(self)
        turnbox_frame.setLayout(QVBoxLayout())

        self.turns_label = QLabel("Turns")
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_frame.layout().addWidget(self.turns_label)

        turnbox_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        turnbox_frame.layout().setContentsMargins(0, 0, 0, 0)
        turnbox_frame.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_frame.layout().setSpacing(0)
        return turnbox_frame

    def resize_GE_turns_widget(self) -> None:
        self.display_manager.update_turn_display()
        self.display_manager.update_adjust_turns_button_size()
