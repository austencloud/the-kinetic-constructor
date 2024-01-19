from typing import TYPE_CHECKING, Dict
from constants import *
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import Colors

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographStateUpdater:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.p = pictograph

    def update_pictograph(self, pictograph_dict: Dict = None) -> None:
        if pictograph_dict:
            if self.p.check.is_pictograph_dict_complete(pictograph_dict):
                self.p.pictograph_dict = pictograph_dict
            self._update_from_pictograph_dict(pictograph_dict)

        self.p.letter_item.update_letter()
        self._position_objects()

    def _update_from_pictograph_dict(self, pictograph_dict: Dict) -> None:
        self.p.attr_manager.update_attributes(pictograph_dict)
        self.update_motion_attrs_from_pictograph_dict(pictograph_dict)
        for motion in self.p.motions.values():
            self.override_motion_type_if_necessary(pictograph_dict, motion)
            if pictograph_dict.get(f"{motion.color}_motion_type"):
                self.show_graphical_objects(motion.color)
            motion.updater.update_motion()

    def show_graphical_objects(self, color: Colors) -> None:
        self.p.props[color].show()
        self.p.ghost_props[color].show()
        self.p.arrows[color].show()

    def override_motion_type_if_necessary(self, pictograph_dict: Dict, motion: Motion):
        motion_type = motion.motion_type
        turns_key = f"{motion_type}_turns"
        if turns_key in pictograph_dict:
            motion.turns = pictograph_dict[turns_key]

    def update_motion_attrs_from_pictograph_dict(self, pictograph_dict):
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

        for attribute_key, attribute_name in motion_attributes.items():
            if attribute_value := pictograph_dict.get(attribute_key):
                setattr(
                    self.p.motions[attribute_key.split("_")[0]],
                    attribute_name,
                    attribute_value,
                )

    def _position_objects(self) -> None:
        self.p.prop_placement_manager.update_prop_positions()
        self.p.arrow_placement_manager.update_arrow_placement()
