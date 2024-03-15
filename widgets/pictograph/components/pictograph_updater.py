from typing import TYPE_CHECKING
from Enums.Enums import LetterType
from Enums.MotionAttributes import Color
from constants import LEADING, TRAILING, RED, BLUE
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographUpdater:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def update_pictograph(self, pictograph_dict: dict = None) -> None:
        """
        Updates the pictograph with the given pictograph_dict.

        If the dict is complete, it will be assigned to the pictograph's pictograph_dict attribute.

        If the dict is incomplete, it will be used to update the pictograph's attributes.

        If there is no dict, the pictograph will update its children without reference to a dict.
        """

        if pictograph_dict:
            if self.pictograph.check.is_pictograph_dict_complete(pictograph_dict):
                self.pictograph.pictograph_dict = pictograph_dict
                self.pictograph.get.initiallize_getter()
                self._update_from_pictograph_dict(pictograph_dict)
                self.pictograph.turns_tuple = self.pictograph.get.turns_tuple()
                self.pictograph.vtg_glyph.set_vtg_mode()
                self.pictograph.elemental_glyph.set_elemental_glyph()
                self.pictograph.container.update_borders()
            else:
                self._update_from_pictograph_dict(pictograph_dict)

        self.pictograph.tka_glyph.update_tka_glyph()  # keep this to update turns
        self._position_objects()

    def _update_from_pictograph_dict(self, pictograph_dict: dict) -> None:
        self.pictograph.attr_manager.update_attributes(pictograph_dict)
        motion_dicts = self.get_motion_dicts_from_pictograph_dict(pictograph_dict)
        for motion in self.pictograph.motions.values():
            self.override_motion_type_if_necessary(pictograph_dict, motion)
            if pictograph_dict.get(
                f"{motion.color}_attributes"
            ) is not None and motion_dicts.get(motion.color) is not None:
            
                self.show_graphical_objects(motion.color)
            motion.updater.update_motion(motion_dicts[motion.color])
        self.pictograph.letter_type = LetterType.get_letter_type(self.pictograph.letter)
        self.pictograph.container.update_borders()

        if self.pictograph.letter_type == LetterType.Type3:
            self.pictograph.get.shift().arrow.updater.update_arrow()
            self.pictograph.get.dash().arrow.updater.update_arrow()
        else:
            for arrow in self.pictograph.arrows.values():
                arrow.updater.update_arrow()
        if self.pictograph.letter in ["S", "T", "U", "V"]:
            self.pictograph.get.leading_motion().lead_state = LEADING
            self.pictograph.get.trailing_motion().lead_state = TRAILING
        else:
            for motion in self.pictograph.motions.values():
                motion.lead_state = None

    def show_graphical_objects(self, color: Color) -> None:
        self.pictograph.props[color].show()
        self.pictograph.arrows[color].show()

    def override_motion_type_if_necessary(
        self, pictograph_dict: dict, motion: Motion
    ) -> None:
        motion_type = motion.motion_type
        turns_key = f"{motion_type}_turns"
        if turns_key in pictograph_dict:
            motion.turns = pictograph_dict[turns_key]

    def get_motion_dicts_from_pictograph_dict(self, pictograph_dict: dict) -> dict:
        # Define which attributes we're interested in for each motion
        motion_attributes = [
            "motion_type",
            "start_loc",
            "end_loc",
            "turns",
            "start_ori",
            "prop_rot_dir",
        ]

        motion_dicts = {}
        for color in [
            RED,
            BLUE,
        ]:  # Assuming RED and BLUE are defined constants for color keys
            # Extract the nested motion dictionary for the current color
            motion_dict = pictograph_dict.get(f"{color}_attributes", {})
            # Filter out the motion attributes to only include the ones we're interested in
            motion_dicts[color] = {
                attr: motion_dict.get(attr)
                for attr in motion_attributes
                if attr in motion_dict
            }

        return motion_dicts

    def _position_objects(self) -> None:
        self.pictograph.prop_placement_manager.update_prop_positions()
        self.pictograph.arrow_placement_manager.update_arrow_placements()

    def update_dict_from_attributes(self) -> dict:
        pictograph_dict = self.pictograph.get.pictograph_dict()
        self.pictograph.pictograph_dict = pictograph_dict
