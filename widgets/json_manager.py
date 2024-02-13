import json
import logging
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget

from widgets.orientation_correction_engine.motion_orientation_json_calculator import (
    SequenceValidationOriCalculator,
)
from widgets.pictograph.components.placement_managers.arrow_placement_manager.components.special_arrow_positioner.managers.special_placement_json_handler import (
    SpecialPlacementJsonHandler,
)


class JSON_Manager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.logger = logging.getLogger(__name__)
        self.special_placement_handler = SpecialPlacementJsonHandler(main_widget)
