import logging
from typing import TYPE_CHECKING

from widgets.current_sequence_json_manager.json_ori_calculator import JsonOriCalculator
from widgets.current_sequence_json_manager.json_sequence_updater import (
    JsonSequenceUpdater,
)
from widgets.current_sequence_json_manager.json_sequence_validation_engine import (
    JsonSequenceValidationEngine,
)
from widgets.current_sequence_json_manager.json_start_position_handler import (
    JsonStartPositionHandler,
)


if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget

from widgets.current_sequence_json_manager.json_sequence_loader_saver import (
    JsonSequenceLoaderSaver,
)
from widgets.pictograph.components.placement_managers.arrow_placement_manager.components.special_arrow_positioner.managers.special_placement_json_handler import (
    SpecialPlacementJsonHandler,
)


class JSON_Manager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.logger = logging.getLogger(__name__)
        self.main_widget = main_widget

        # special placement
        self.special_placement_handler = SpecialPlacementJsonHandler()

        # current sequence
        self.loader_saver = JsonSequenceLoaderSaver(self)
        self.updater = JsonSequenceUpdater(self)
        self.start_position_handler = JsonStartPositionHandler(self)
        self.ori_calculator = JsonOriCalculator(self)
        self.validation_engine = JsonSequenceValidationEngine(self)
