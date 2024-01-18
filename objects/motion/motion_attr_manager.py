from typing import TYPE_CHECKING, Dict, Union
from constants import (
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    DASH,
    END_LOC,
    END_ORI,
    MOTION_TYPE,
    NO_ROT,
    OPP,
    PROP,
    PROP_ROT_DIR,
    RED,
    SAME,
    START_LOC,
    START_ORI,
    STATIC,
    TURNS,
)
from utilities.TypeChecking.TypeChecking import Orientations
from widgets.filter_tab import FilterTab

if TYPE_CHECKING:
    from widgets.attr_box.attr_box import AttrBox
    from objects.motion.motion import Motion


class MotionAttrManager:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def update_attributes(self, motion_dict: Dict[str, str]) -> None:
        for attribute, value in motion_dict.items():
            if value is not None:
                setattr(self, attribute, value)
        if self.motion.motion_type:
            self.motion.end_ori: Orientations = self.motion.ori_calculator.get_end_ori()


    def update_motion_attributes_from_filter_tab(
        self, filter_tab: "FilterTab", pictograph_dict: Dict
    ) -> None:
        for box in filter_tab.motion_type_attr_panel.boxes:
            if (
                box.attribute_type == MOTION_TYPE
                and box.motion_type
                == pictograph_dict.get(f"{self.motion.color}_{MOTION_TYPE}")
            ):
                self.set_motion_attributes_from_attr_box(box, pictograph_dict)

    def set_motion_attributes_from_attr_box(
        self, box: "AttrBox", pictograph_dict: Dict
    ) -> None:
        box_text = box.turns_widget.turns_display_manager.turns_display.text()
        turns = float(box_text) if "." in box_text else int(box_text)

        if box.motion_type in [DASH, STATIC]:
            self.set_motion_turns_and_direction_from_attr_box(
                box, pictograph_dict, turns
            )

    def set_motion_turns_and_direction_from_attr_box(
        self, box: "AttrBox", pictograph_dict: Dict, turns: Union[int, float]
    ) -> None:
        if box.vtg_dir_btn_state[SAME]:
            self.set_same_direction_turns_from_attr_box(box, pictograph_dict, turns)
        elif box.vtg_dir_btn_state[OPP]:
            self.set_opposite_direction_turns_from_attr_box(box, pictograph_dict, turns)

        if turns == 0 and pictograph_dict[self.motion.color + "_" + MOTION_TYPE] in [
            DASH,
            STATIC,
        ]:
            pictograph_dict[self.motion.color + "_" + PROP_ROT_DIR] = NO_ROT

    def set_same_direction_turns_from_attr_box(
        self, box: "AttrBox", pictograph_dict: Dict, turns: Union[int, float]
    ) -> None:
        other_color = RED if self.motion.color == BLUE else BLUE
        if pictograph_dict[self.motion.color + "_" + MOTION_TYPE] == box.motion_type:
            pictograph_dict[self.motion.color + "_" + PROP_ROT_DIR] = pictograph_dict[
                other_color + "_" + PROP_ROT_DIR
            ]
            pictograph_dict[self.motion.color + "_" + TURNS] = turns

    def set_opposite_direction_turns_from_attr_box(
        self, box: "AttrBox", pictograph_dict: Dict, turns: Union[int, float]
    ) -> None:
        other_color = RED if self.motion.color == BLUE else BLUE
        opposite_dir = (
            COUNTER_CLOCKWISE
            if pictograph_dict[other_color + "_" + PROP_ROT_DIR] == CLOCKWISE
            else CLOCKWISE
        )
        if pictograph_dict[self.motion.color + "_" + MOTION_TYPE] == box.motion_type:
            pictograph_dict[self.motion.color + "_" + PROP_ROT_DIR] = opposite_dir
            pictograph_dict[self.motion.color + "_" + TURNS] = turns

    def update_prop_ori(self) -> None:
        if hasattr(self.motion, PROP) and self.motion.prop:
            if not self.motion.end_ori:
                self.motion.end_ori = self.motion.ori_calculator.get_end_ori()
            self.motion.prop.ori = self.motion.end_ori
            self.motion.prop.loc = self.motion.end_loc
            self.motion.prop.axis = self.motion.prop.get_axis_from_ori()

    def get_attributes(self) -> Dict[str, str]:
        return {
            COLOR: self.motion.color,
            MOTION_TYPE: self.motion.motion_type,
            TURNS: self.motion.turns,
            PROP_ROT_DIR: self.motion.prop_rot_dir,
            START_LOC: self.motion.start_loc,
            END_LOC: self.motion.end_loc,
            START_ORI: self.motion.start_ori,
            END_ORI: self.motion.end_ori,
        }
