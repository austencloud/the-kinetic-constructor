from typing import TYPE_CHECKING, Dict
from PyQt6.QtSvg import QSvgRenderer
from constants import *
from utilities.TypeChecking.TypeChecking import Colors

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    pass


class PictographStateUpdater:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def update_attributes(self, pictograph_dict: Dict) -> None:
        for attr_name, attr_value in pictograph_dict.items():
            setattr(self.pictograph, attr_name, attr_value)

    def update_pictograph(self, pictograph_dict: Dict = None) -> None:
        if pictograph_dict:
            if self.pictograph.is_pictograph_dict_complete(pictograph_dict):
                self.pictograph.pictograph_dict = pictograph_dict
            self._update_from_pictograph_dict(pictograph_dict)

        self.update_letter()
        self._position_objects()

    def _update_from_pictograph_dict(self, pictograph_dict: Dict) -> None:
        self.update_attributes(pictograph_dict)
        motion_dicts = []
        if LETTER in pictograph_dict:
            self.pictograph.letter = pictograph_dict[LETTER]
            self.pictograph.letter_type = self.pictograph._get_letter_type(
                self.pictograph.letter
            )
        if PRO_TURNS in pictograph_dict:
            pro_motion = (
                self.pictograph.blue_motion
                if self.pictograph.blue_motion.motion_type == PRO
                else self.pictograph.red_motion
            )
            pro_motion.turns = pictograph_dict[PRO_TURNS]

        if ANTI_TURNS in pictograph_dict:
            anti_motion = (
                self.pictograph.blue_motion
                if self.pictograph.blue_motion.motion_type == ANTI
                else self.pictograph.red_motion
            )
            anti_motion.turns = pictograph_dict[ANTI_TURNS]

        if DASH_TURNS in pictograph_dict:
            dash_motion = (
                self.pictograph.blue_motion
                if self.pictograph.blue_motion.motion_type == DASH
                else self.pictograph.red_motion
            )
            dash_motion.turns = pictograph_dict[DASH_TURNS]

        if STATIC_TURNS in pictograph_dict:
            static_motion = (
                self.pictograph.blue_motion
                if self.pictograph.blue_motion.motion_type == STATIC
                else self.pictograph.red_motion
            )
            static_motion.turns = pictograph_dict[STATIC_TURNS]

        for color in [BLUE, RED]:
            motion_dict = self._create_motion_dict(pictograph_dict, color)
            motion_dicts.append(motion_dict)
            if MOTION_TYPE in motion_dict:
                self.pictograph.motions[color].motion_type = motion_dict[MOTION_TYPE]
            if PROP_ROT_DIR in motion_dict:
                self.pictograph.motions[color].prop_rot_dir = motion_dict[PROP_ROT_DIR]
            if START_ORI in motion_dict:
                self.pictograph.motions[color].start_ori = motion_dict[START_ORI]
            if START_LOC in motion_dict:
                self.pictograph.motions[color].start_loc = motion_dict[START_LOC]
            if END_LOC in motion_dict:
                self.pictograph.motions[color].end_loc = motion_dict[END_LOC]
            if TURNS in motion_dict:
                self.pictograph.motions[color].turns = motion_dict[TURNS]
            if pictograph_dict.get(f"{color}_motion_type"):
                arrow_dict = {
                    MOTION_TYPE: pictograph_dict.get(f"{color}_motion_type"),
                    TURNS: pictograph_dict.get(f"{color}_turns"),
                }

                self.pictograph.motions[color].arrow.setup_arrow(arrow_dict)
                self.pictograph.ghost_arrows[color].setup_arrow(arrow_dict)
                self.pictograph.motions[color].arrow.show()
                prop_dict = {
                    PROP_ROT_DIR: pictograph_dict.get(f"{color}_prop_rot_dir"),
                    ORI: self.pictograph.motions[color].get_end_ori(),
                }
                self.pictograph.motions[color].prop.update_attributes(prop_dict)
                self.pictograph.ghost_props[color].update_attributes(prop_dict)
                self.pictograph.motions[color].prop.show()
                self.pictograph.motions[color].prop.update_prop()

        self._update_motions()

    def _create_motion_dict(self, pictograph_dict: Dict, color: Colors) -> Dict:
        motion_dict = {
            COLOR: color,
            MOTION_TYPE: pictograph_dict.get(f"{color}_motion_type"),
            PROP_ROT_DIR: pictograph_dict.get(f"{color}_prop_rot_dir"),
            START_LOC: pictograph_dict.get(f"{color}_start_loc"),
            END_LOC: pictograph_dict.get(f"{color}_end_loc"),
            TURNS: pictograph_dict.get(f"{color}_turns"),
            START_ORI: pictograph_dict.get(f"{color}_start_ori"),
        }
        return {k: v for k, v in motion_dict.items() if v != None}

    def _update_attr_panel(self) -> None:
        for motion in self.pictograph.motions.values():
            self.pictograph.main_widget.graph_editor_tab.graph_editor.attr_panel.update_attr_panel(
                motion
            )

    def _position_objects(self) -> None:
        self.pictograph.prop_placement_manager.update_prop_positions()
        self.pictograph.arrow_placement_manager.update_arrow_placement()

    def _update_motions(self) -> None:
        for motion in self.pictograph.motions.values():
            motion.update_motion()

    def update_letter(self) -> None:
        if all(motion.motion_type for motion in self.pictograph.motions.values()):
            self.pictograph.letter = self.pictograph.letter_engine.get_current_letter()
            self.pictograph.letter_item.letter = self.pictograph.letter
            self.pictograph._set_letter_renderer(self.pictograph.letter)
            self.pictograph.letter_item.position_letter_item(
                self.pictograph.letter_item
            )
        else:
            self.pictograph.letter = None
            svg_path = f"resources/images/letter_button_icons/blank.svg"
            renderer = QSvgRenderer(svg_path)
            if renderer.isValid():
                self.pictograph.letter_item.setSharedRenderer(renderer)
