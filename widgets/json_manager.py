import logging
from typing import TYPE_CHECKING
from widgets.current_sequence_json_handler.current_sequence_json_handler import CurrentSequenceJsonHandler


if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget

from widgets.pictograph.components.placement_managers.arrow_placement_manager.components.special_arrow_positioner.managers.special_placement_json_handler import (
    SpecialPlacementJsonHandler,
)


class JSON_Manager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.logger = logging.getLogger(__name__)
        self.special_placement_handler = SpecialPlacementJsonHandler(main_widget)
        self.current_sequence_json_handler = CurrentSequenceJsonHandler(main_widget)