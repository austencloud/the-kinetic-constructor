from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )


class RotationalAndColorSwappedPermutationChecker:
    def __init__(self, manager: "SequencePropertiesManager"):
        self.manager = manager

    def check(self) -> bool:
        pass
