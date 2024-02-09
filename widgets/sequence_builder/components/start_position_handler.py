from typing import TYPE_CHECKING
from constants import END_POS, START_POS
from ...pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_builder.sequence_builder import SequenceBuilder


class StartPositionHandler:
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        self.start_options: dict[str, Pictograph] = {}
        self.sequence_builder = sequence_builder
