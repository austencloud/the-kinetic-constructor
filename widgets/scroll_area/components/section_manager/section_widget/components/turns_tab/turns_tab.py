from PyQt6.QtWidgets import QTabWidget

from Enums.Enums import TurnsTabAttribute
from .turns_tab_visibility_handler import TurnsTabVisibilityHandler
from typing import TYPE_CHECKING
from .turns_tab_turns_updater import TurnsTabUpdater
from widgets.turns_panel import GE_AdjustmentPanel

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from widgets.scroll_area.components.section_manager.section_widget.codex_section_widget import (
        CodexSectionWidget,
    )


class TurnsTab(QTabWidget):
    def __init__(self, section: "CodexSectionWidget"):
        super().__init__()
        self.section = section

        self._setup_panels()
        self._setup_handlers()
        self.currentChanged.connect(self.section.reset_section)

    def _setup_handlers(self):
        self.visibility_handler = TurnsTabVisibilityHandler(self)
        self.updater = TurnsTabUpdater(self)

    def _setup_panels(self):
        self.motion_type_turns_panel = GE_AdjustmentPanel(
            self, TurnsTabAttribute.MOTION_TYPE
        )
        self.color_turns_panel = GE_AdjustmentPanel(self, TurnsTabAttribute.COLOR)
        self.lead_state_turns_panel = GE_AdjustmentPanel(
            self, TurnsTabAttribute.LEAD_STATE
        )

        self.panels = [
            self.motion_type_turns_panel,
            self.color_turns_panel,
            self.lead_state_turns_panel,
        ]

    def apply_turns_to_pictographs(self, pictograph: "Pictograph"):
        self.updater.apply_turns(pictograph)

    def get_current_turns_values(self) -> dict[str, dict[str, int]]:
        turns_values = {}
        for panel in [
            self.motion_type_turns_panel,
            self.color_turns_panel,
            self.lead_state_turns_panel,
        ]:
            for box in panel.boxes:
                if box.attribute_type not in turns_values:
                    turns_values[box.attribute_type] = {}
                turns_values[box.attribute_type][
                    box.attribute_value
                ] = box.turns_widget.display_manager.get_current_turns_value()
        return turns_values
