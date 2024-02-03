from Enums import LetterType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mirrored_entry_manager import SpecialPlacementMirroredEntryManager


class MirroredEntryPictographSectionUpdater:
    def __init__(self, manager: "SpecialPlacementMirroredEntryManager"):
        self.manager = manager

    def update_pictographs_in_section(self, letter_type: LetterType):
        """
        Triggers an update of the pictographs in the section corresponding to the given letter type.
        This method ensures that the UI reflects the most current data after changes have been made to the mirrored entries.
        """
        section = self.manager.data_updater.positioner.pictograph.scroll_area.sections_manager.get_section(
            letter_type
        )
        for _, pictograph in section.pictographs.items():
            pictograph.arrow_placement_manager.update_arrow_placements()
