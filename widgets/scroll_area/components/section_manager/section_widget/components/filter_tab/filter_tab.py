from PyQt6.QtWidgets import QTabWidget
from .filter_tab_visibility_handler import FilterTabVisibilityHandler
from typing import TYPE_CHECKING
from constants import MOTION_TYPE, COLOR, LEAD_STATE
from .filter_tab_turns_updater import FilterTabTurnsUpdater
from widgets.turns_panel import TurnsPanel

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from widgets.scroll_area.components.section_manager.section_widget.section_widget import (
        SectionWidget,
    )


class FilterTab(QTabWidget):
    def __init__(self, section: "SectionWidget"):
        super().__init__()
        self.section = section

        # Instantiate panels
        self.motion_type_turns_panel = TurnsPanel(self, MOTION_TYPE)
        self.color_turns_panel = TurnsPanel(self, COLOR)
        self.lead_state_turns_panel = TurnsPanel(self, LEAD_STATE)

        self.panels = [
            self.motion_type_turns_panel,
            self.color_turns_panel,
            self.lead_state_turns_panel,
        ]

        # Setup managers
        self.visibility_handler = FilterTabVisibilityHandler(self)
        self.turns_updater = FilterTabTurnsUpdater(self)

    def apply_turns_to_pictographs(self, pictograph: "Pictograph"):
        self.turns_updater.apply_turns(pictograph)

    def get_current_turns_values(self) -> dict[str, dict[str, int]]:
        turns_values = {}
        for panel in [
            self.motion_type_turns_panel,
            self.color_turns_panel,
            self.lead_state_turns_panel,
        ]:
            for box in panel.boxes:
                turns_values[box.attribute_type] = (
                    box.turns_widget.display_manager.get_current_turns_value()
                )
        return turns_values
