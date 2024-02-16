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
            if pictograph_dict.get(f"{motion.color.value}_motion_type"):
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
        motion_attributes = {
            f"{RED}_motion_type": "motion_type",
            f"{RED}_start_loc": "start_loc",
            f"{RED}_end_loc": "end_loc",
            f"{RED}_turns": "turns",
            f"{RED}_start_ori": "start_ori",
            f"{RED}_prop_rot_dir": "prop_rot_dir",
            f"{BLUE}_motion_type": "motion_type",
            f"{BLUE}_start_loc": "start_loc",
            f"{BLUE}_end_loc": "end_loc",
            f"{BLUE}_turns": "turns",
            f"{BLUE}_start_ori": "start_ori",
            f"{BLUE}_prop_rot_dir": "prop_rot_dir",
        }
        motion_dicts = {}
        for color in [Color.RED, Color.BLUE]:
            motion_dict = {}
            for key, value in motion_attributes.items():
                if color.value in key and key in pictograph_dict:
                    motion_dict[key.split("_", 1)[1]] = pictograph_dict[key]
            motion_dicts[color] = motion_dict
        return motion_dicts

    def _position_objects(self) -> None:
        self.pictograph.prop_placement_manager.update_prop_positions()
        self.pictograph.arrow_placement_manager.update_arrow_placements()
