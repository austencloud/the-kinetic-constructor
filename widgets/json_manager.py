import logging
from typing import TYPE_CHECKING
from widgets.current_sequence_json_manager.current_sequence_json_manager import (
    CurrentSequenceJsonManager,
)


if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget

from widgets.pictograph.components.placement_managers.arrow_placement_manager.components.special_arrow_positioner.managers.special_placement_json_handler import (
    SpecialPlacementJsonHandler,
)


class JSON_Manager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.logger = logging.getLogger(__name__)
        self.main_widget = main_widget
        self.special_placement_handler = SpecialPlacementJsonHandler()
        self.current_sequence_json_manager = CurrentSequenceJsonManager(self)
