import logging
from typing import TYPE_CHECKING
from .json_ori_calculator import JsonOriCalculator
from .json_sequence_updater import JsonSequenceUpdater
from .json_sequence_validation_engine import JsonSequenceValidationEngine
from .json_start_position_handler import JsonStartPositionHandler
from .json_sequence_loader_saver import JsonSequenceLoaderSaver
from .json_special_placement_handler import JsonSpecialPlacementHandler

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget

class JSON_Manager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.logger = logging.getLogger(__name__)

        # special placement
        self.special_placement_handler = JsonSpecialPlacementHandler(self)

        # current sequence
        self.loader_saver = JsonSequenceLoaderSaver(self)
        self.updater = JsonSequenceUpdater(self)
        self.start_position_handler = JsonStartPositionHandler(self)
        self.ori_calculator = JsonOriCalculator(self)
        self.validation_engine = JsonSequenceValidationEngine(self)
