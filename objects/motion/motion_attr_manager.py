from typing import TYPE_CHECKING, Dict, Union
from constants import (
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    DASH,
    END_LOC,
    END_ORI,
    LEADING,
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
    TRAILING,
    TURNS,
)
from utilities.TypeChecking.TypeChecking import Colors, Orientations, Turns
from widgets.filter_tab import FilterTab

if TYPE_CHECKING:
    from widgets.attr_box.attr_box import AttrBox
    from objects.motion.motion import Motion


class MotionAttrManager:
    def __init__(self, motion: "Motion") -> None:
        self.m = motion
        self.m.color: Colors = self.m.motion_dict.get(COLOR)
        self.m.turns: Turns = self.m.motion_dict.get(TURNS)
        self.m.start_loc = None
        self.m.end_loc = None
        self.m.motion_type = None

    def update_attributes(self, motion_dict: Dict[str, str]) -> None:
        for attribute, value in motion_dict.items():
            if value is not None:
                setattr(self.m, attribute, value)

        if self.m.motion_type:
            self.m.end_ori: Orientations = self.m.ori_calculator.get_end_ori()

    def update_motion_attributes_from_filter_tab(
        self, filter_tab: "FilterTab", pictograph_dict: Dict
    ) -> None:
        for box in filter_tab.motion_type_attr_panel.boxes:
            if (
                box.attribute_type == MOTION_TYPE
                and box.motion_type
                == pictograph_dict.get(f"{self.m.color}_{MOTION_TYPE}")
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

        if turns == 0 and pictograph_dict[self.m.color + "_" + MOTION_TYPE] in [
            DASH,
            STATIC,
        ]:
            pictograph_dict[self.m.color + "_" + PROP_ROT_DIR] = NO_ROT

    def set_same_direction_turns_from_attr_box(
        self, box: "AttrBox", pictograph_dict: Dict, turns: Union[int, float]
    ) -> None:
        other_color = RED if self.m.color == BLUE else BLUE
        if pictograph_dict[self.m.color + "_" + MOTION_TYPE] == box.motion_type:
            pictograph_dict[self.m.color + "_" + PROP_ROT_DIR] = pictograph_dict[
                other_color + "_" + PROP_ROT_DIR
            ]
            pictograph_dict[self.m.color + "_" + TURNS] = turns

    def set_opposite_direction_turns_from_attr_box(
        self, box: "AttrBox", pictograph_dict: Dict, turns: Union[int, float]
    ) -> None:
        other_color = RED if self.m.color == BLUE else BLUE
        opposite_dir = (
            COUNTER_CLOCKWISE
            if pictograph_dict[other_color + "_" + PROP_ROT_DIR] == CLOCKWISE
            else CLOCKWISE
        )
        if pictograph_dict[self.m.color + "_" + MOTION_TYPE] == box.motion_type:
            pictograph_dict[self.m.color + "_" + PROP_ROT_DIR] = opposite_dir
            pictograph_dict[self.m.color + "_" + TURNS] = turns

    def update_prop_ori(self) -> None:
        if hasattr(self.m, PROP) and self.m.prop:
            if not self.m.end_ori:
                self.m.end_ori = self.m.ori_calculator.get_end_ori()
            self.m.prop.ori = self.m.end_ori
            self.m.prop.loc = self.m.end_loc
            self.m.prop.axis = self.m.prop.attr_manager.get_axis_from_ori()

    def get_attributes(self) -> Dict[str, str]:
        return {
            COLOR: self.m.color,
            MOTION_TYPE: self.m.motion_type,
            TURNS: self.m.turns,
            PROP_ROT_DIR: self.m.prop_rot_dir,
            START_LOC: self.m.start_loc,
            END_LOC: self.m.end_loc,
            START_ORI: self.m.start_ori,
            END_ORI: self.m.end_ori,
        }

    def _change_motion_attributes_to_static(self) -> None:
        motion_dict = {
            MOTION_TYPE: STATIC,
            TURNS: 0,
            PROP_ROT_DIR: NO_ROT,
            START_LOC: self.m.prop.loc,
            END_LOC: self.m.prop.loc,
        }
        self.m.updater.update_motion(motion_dict)
        self.m.arrow.loc = self.m.prop.loc
