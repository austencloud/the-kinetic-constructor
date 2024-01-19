from typing import TYPE_CHECKING, Dict
from PyQt6.QtSvg import QSvgRenderer
from Enums import LetterNumberType
from constants import *
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import Colors

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    pass


class PictographStateUpdater:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.p = pictograph

    def update_pictograph(self, pictograph_dict: Dict = None) -> None:
        if pictograph_dict:
            if self.p.is_pictograph_dict_complete(pictograph_dict):
                self.p.pictograph_dict = pictograph_dict
            self._update_from_pictograph_dict(pictograph_dict)

        self.update_letter()
        self._position_objects()

    def _update_from_pictograph_dict(self, pictograph_dict: Dict) -> None:
        self.p.attr_manager.update_attributes(pictograph_dict)
        self.update_motion_attrs_from_pictograph_dict(pictograph_dict)
        for color in [BLUE, RED]:
            motion = self.p.motions[color]
            arrow = self.p.arrows[color]
            prop = self.p.props[color]
            ghost_prop = self.p.ghost_props[color]
            motion = self.p.blue_motion if color == BLUE else self.p.red_motion
            self.override_motion_type_if_necessary(pictograph_dict, motion)
            if pictograph_dict.get(f"{color}_motion_type"):
                arrow.show()
                prop_dict = {
                    PROP_ROT_DIR: pictograph_dict.get(f"{color}_prop_rot_dir"),
                    ORI: motion.ori_calculator.get_end_ori(),
                }
                ghost_prop.attr_manager.update_attributes(prop_dict)
                prop.attr_manager.update_attributes(prop_dict)
                prop.show()
                prop.loc = motion.end_loc
                prop.ghost.loc = motion.end_loc
                prop.ori = self.p.motions[color].ori_calculator.get_end_ori()
        
        for motion in self.p.motions.values():
            motion.updater.update_motion()


    def override_motion_type_if_necessary(self, pictograph_dict: Dict, motion: Motion):
        motion_type = motion.motion_type
        turns_key = f"{motion_type}_turns"
        if turns_key in pictograph_dict:
            motion.turns = pictograph_dict[turns_key]

    def update_motion_attrs_from_pictograph_dict(self, pictograph_dict):
        motion_attributes = {
            f"{RED}_motion_type": "motion_type",
            f"{BLUE}_motion_type": "motion_type",
            f"{RED}_start_loc": "start_loc",
            f"{BLUE}_start_loc": "start_loc",
            f"{RED}_end_loc": "end_loc",
            f"{BLUE}_end_loc": "end_loc",
            f"{RED}_turns": "turns",
            f"{BLUE}_turns": "turns",
            f"{RED}_start_ori": "start_ori",
            f"{BLUE}_start_ori": "start_ori",
            f"{RED}_prop_rot_dir": "prop_rot_dir",
            f"{BLUE}_prop_rot_dir": "prop_rot_dir",
        }

        for attribute_key, attribute_name in motion_attributes.items():
            if attribute_value := pictograph_dict.get(attribute_key):
                setattr(
                    self.p.motions[attribute_key.split("_")[0]],
                    attribute_name,
                    attribute_value,
                )

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
        for motion in self.p.motions.values():
            self.p.main_widget.graph_editor_tab.graph_editor.attr_panel.update_attr_panel(
                motion
            )

    def _position_objects(self) -> None:
        self.p.prop_placement_manager.update_prop_positions()
        self.p.arrow_placement_manager.update_arrow_placement()

    def _update_motions(self) -> None:
        for motion in self.p.motions.values():
            motion.updater.update_motion()

    def update_letter(self) -> None:
        if all(motion.motion_type for motion in self.p.motions.values()):
            self.p.letter = self.p.letter_engine.get_current_letter()
            self.p.letter_type = self.get_letter_type(self.p.letter)
            self.p.letter_item.letter = self.p.letter
            self.p._set_letter_renderer(self.p.letter)
            self.p.letter_item.position_letter_item(self.p.letter_item)
        else:
            self.p.letter = None
            svg_path = f"resources/images/letter_button_icons/blank.svg"
            renderer = QSvgRenderer(svg_path)
            if renderer.isValid():
                self.p.letter_item.setSharedRenderer(renderer)

    # Function to get the Enum member key from a given letter
    def get_letter_type(self, letter: str) -> str | None:
        for letter_type in LetterNumberType:
            if letter in letter_type.letters:
                return letter_type.name.replace("_", "").lower().capitalize()
        return None
